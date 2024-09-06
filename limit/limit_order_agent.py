from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        self.orders = []
        super().__init__()
        self.execution_client = execution_client
        

    def on_price_tick(self, product_id: str, price: float) -> None:
        # see PriceListener protocol and readme file
        """
        Method executes whenever there is a new market price
        @param product_id : The ID of the product
        @param price : The new market price of the product
        """
        try:
            for order in self.orders:
                if order.get("product_id","") == product_id:
                    amount = order.get("amount", 0)
                    if order.get('action') == 'buy' and price <=amount:
                        print(f"Buying {amount} of product {product_id}")
                        self.execution_client.buy(product_id, amount)
                        self.orders.remove(order)
                    elif order.get('action') == 'sell' and price >= amount:
                        print(f"Selling {amount} of product {product_id}")
                        self.execution_client.buy(product_id, amount) 
                        self.orders.remove(order)                       
        except Exception as e:
            print(f"Exception at on price tick : {e}")
    
    def add_order(self, action:bool, product_id:str, amount:int, limit:float) -> None:
        """
        Method to accept the order
        @param is_buy : flag indicates buy or sell
        @param product_id : id of the product
        @param amount : the amount to buy or sell
        @param limit : the limit at which to buy or sell

        """
        if action == '':
            raise Exception("Provide the value as buy or sell")
        elif product_id == '':
            raise Exception("Provide the valid product id")
        elif amount == '':
            raise Exception("Provide the valid amount")
        elif limit == '':
            raise Exception("Provide the valid limit")
        else:
            self.orders.append({"action" : action,
                                "product_id" :product_id,
                                "amount" : amount,
                                "limit" : limit 
                                })




