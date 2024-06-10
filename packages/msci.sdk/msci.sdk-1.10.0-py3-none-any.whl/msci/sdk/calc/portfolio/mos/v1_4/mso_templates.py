from typing import List

from .client_portfolio import TaxLotPortfolio, ClientPortfolio, SimplePortfolio, CashPortfolio
from .constraints import ConstraintFactory
from .enums import MultiAccountStyleEnum
from .full_optimizer_node import FullSpecOptimizationNode, GenericObjectiveFunction, OptimizationSettings, \
    TaxOptimizationSetting
from .mos_config import Strategy, ReferenceUniverse, BenchmarkPerAccount, UniversePerAccount, \
    CurrentPortfolioPerAccount, NodeListPerAccount, SimulationSettings
from .profile import Profile


class SleeveConfig:
    """
    A sleeve configuration for the MSO template.

    Args:
        id (str): The id or name of the sleeve.
        target (float): The target weight of the sleeve.
        drift (float): The drift of the sleeve.
        te_limit (float): The tracking error limit of the sleeve.
        benchmark_list (List): A list of benchmarks.
        universe_list (List): A list of universes.
        portfolio (CashPortfolio|TaxLotPortfolio|SimplePortfolio|ClientPortfolio): The portfolio.
        cash_upper_bound (float): The upper bound of cash.
        cash_lower_bound (float): The lower bound of cash.
        constraints (List): A list of constraints.
        prefix_nodes (List): A list of prefix nodes.

    """
    def __init__(
            self,
            id: str,
            target: float,
            drift: float,
            te_limit: float,
            benchmark_list: List,
            universe_list: List,
            portfolio,
            cash_upper_bound: float = 0.0,
            cash_lower_bound: float = 0.0,
            constraints: List = None,
            prefix_nodes: List = None
    ):
        self.id = id
        self.target = target
        self.drift = drift
        self.te_limit = te_limit
        self.benchmark_list = benchmark_list
        self.universe_list = universe_list
        self.portfolio = portfolio
        self.cash_upper_bound = cash_upper_bound
        self.cash_lower_bound = cash_lower_bound
        self.constraints = constraints
        self.prefix_nodes = prefix_nodes


class MSOTemplate(Profile):
    """
    A template for a Multi-Sleeve Optimization (MSO) profile.

    Args:
        sleeves_config (List[SleeveConfig]): A list of sleeve configurations.
        analysis_date: The date of the analysis.
        global_te_limit: The global tracking error limit.
        benchmark_list (List): A list of benchmarks.
        universe_list (List): A list of universes.
        portfolio (CashPortfolio|TaxLotPortfolio|SimplePortfolio|ClientPortfolio): The portfolio.
        cash_upper_bound (float): The upper bound of cash.
        cash_lower_bound (float): The lower bound of cash.
        global_constraints (List): A list of global constraints.
        global_prefix_nodes (List): A list of global prefix nodes.
        profile_name (str): The name of the profile.

    """
    def __init__(
            self,
            sleeves_config: List[SleeveConfig],
            analysis_date,
            global_te_limit,
            benchmark_list: List,
            universe_list: List,
            portfolio,
            cash_upper_bound: float = 0.0,
            cash_lower_bound: float = 0.0,
            global_constraints: List = None,
            global_prefix_nodes: List = None,
            profile_name: str = None
    ):

        sleeve_ids = []
        bmk_sleeves = []
        univ_sleeves = []
        portfolio_sleeves = []

        for sleeve in sleeves_config:
            sleeve_ids.append(sleeve.id)
            bmk_sleeves += [BenchmarkPerAccount(account_id=sleeve.id, benchmark=sleeve.benchmark_list)]
            univ_sleeves += [UniversePerAccount(account_id=sleeve.id, universe=sleeve.universe_list)]
            portfolio_sleeves += [CurrentPortfolioPerAccount(account_id=sleeve.id, portfolio=sleeve.portfolio)]

        ref_univ = ReferenceUniverse(benchmark_multi_account=bmk_sleeves,
                                     universe_multi_account=univ_sleeves,
                                     current_portfolio_multi_account=portfolio_sleeves,
                                     universe=universe_list,
                                     benchmark=benchmark_list,
                                     portfolio=portfolio
                                     )

        bmk_ref_names = ref_univ.get_benchmark_ref_name()

        sleeve_optimization_nodes = []

        for sleeve in sleeves_config:
            sleeve_target = ConstraintFactory.SleeveBalanceConstraint(lower_bound=f'{sleeve.target - sleeve.drift}',
                                                                      upper_bound=f'{sleeve.target + sleeve.drift}')

            sleeve_te = ConstraintFactory.RiskConstraint(reference_portfolio=bmk_ref_names[
                bmk_ref_names['account_id'] == sleeve.id]['benchmark_ref_name'].reset_index(drop=True)[0],
                                                         upper_bound=sleeve.te_limit)

            if sleeve.constraints:
                sleeve_constraints = sleeve.constraints + [sleeve_target, sleeve_te]
            else:
                sleeve_constraints = [sleeve_target, sleeve_te]
            sleeve_opt_settings = OptimizationSettings(
                cash_in_portfolio_upper_bound=sleeve.cash_upper_bound,
                cash_in_portfolio_lower_bound=sleeve.cash_lower_bound
            )
            optimization_node = FullSpecOptimizationNode(constraints=sleeve_constraints,
                                                         opt_settings=sleeve_opt_settings)

            if sleeve.prefix_nodes:
                sleeve_node_list = sleeve.prefix_nodes + [optimization_node]
            else:
                sleeve_node_list = [optimization_node]
            sleeve_optimization_nodes += [
                NodeListPerAccount(account_id=sleeve.id, node_list=sleeve_node_list)]

        opt_settings = OptimizationSettings(
            transaction_type='allowAll',
            cash_in_portfolio_upper_bound=cash_upper_bound,
            cash_in_portfolio_lower_bound=cash_lower_bound,
            tax_optimization_setting=TaxOptimizationSetting(tax_unit="amount", selling_order_rule="auto",
                                                            long_term_tax_rate=0.238, short_term_tax_rate=0.408,
                                                            wash_sale_rule="disallowed")
        )
        obj_function = GenericObjectiveFunction(
            tax_term=1,
            loss_benefit_term=0,
            sp_risk_aversion=0.01,
            cf_risk_aversion=0.01,
            minimize_active_risk=False
        )

        if global_constraints:
            shared_constraints = global_constraints + [ConstraintFactory.AggregateRiskConstraint(
                upper_bound=global_te_limit)]
        else:
            shared_constraints = [ConstraintFactory.AggregateRiskConstraint(upper_bound=global_te_limit)]

        shared_optimization_node = FullSpecOptimizationNode(opt_settings=opt_settings,
                                                            objective_function=obj_function,
                                                            constraints=shared_constraints)

        if global_prefix_nodes:
            node_list = global_prefix_nodes + [shared_optimization_node]
        else:
            node_list = [shared_optimization_node]

        shared_strategy = Strategy(
            ref_universe=ref_univ,
            node_list=node_list,
            node_list_multi_account=sleeve_optimization_nodes
        )

        sim_settings = SimulationSettings(analysis_date=analysis_date,
                                          account_ids=sleeve_ids,
                                          multi_account_style=MultiAccountStyleEnum.MULTI_SLEEVE)

        super().__init__(
            strategy=shared_strategy,
            simulation_settings=sim_settings,
            profile_name=profile_name
        )
