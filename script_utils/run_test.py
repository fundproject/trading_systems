
from vnpy.gateway.uft import UftGateway

from vnpy.app.script_trader import ScriptTraderApp, init_cli_trading


stage_setting = {
    "用户名": "30010074",
    "密码": "199406",
    "交易服务器": "116.236.247.243:21491",  # 模拟交易
    "行情服务器": "116.236.247.243:21492",  # 模拟行情
    "服务器类型": "ETF期权",
    "产品名称": "",
    "授权编码": "",
    "委托类型": "7"
}
def main():
    """"""
    engine = init_cli_trading([UftGateway])
    engine.connect_gateway(stage_setting, "UFT")

    contract_info = engine.get_all_contracts(True)
    print(contract_info)

if __name__ == "__main__":
    main()

