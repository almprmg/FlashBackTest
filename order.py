class orders:

    def __init__(self) -> None:
        self.order =None
        self.tp = None
        self.sl = None
        self.limet =None
        self.Date_ende_order = None
        self._postin =True

        
    def buy(self, limet:float,tp: float,sl:float)-> None:
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self.limet =limet
            self.order[["DateStart","Enter","tp","ls"]] = [self.Date,limet,tp,sl]
            self._postin = True

            

            
    def sell(self, limet:float,tp: float,sl:float):
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self._postin = True



    def TpOredes_Buy(self,Date_TP):
        self.order[[ "Targit","EndDate"]] = [1,Date_TP]
        self.Date_ende_order = Date_TP
        self._postin =False
    def SlOredes_Buy(self,Date_SL):
        self.order[[ "Targit","EndDate"]] = [0,Date_SL]
        self.Date_ende_order = Date_SL
        self._postin =False
    def TpOredes_Sell(self,Date_TP):
        self.order[[ "Targit","EndDate"]] = [2,Date_TP]
        self.Date_ende_order = Date_TP
        self._postin =False
    def SlOredes_Sell(self,Date_SL):
        self.order[[ "Targit","EndDate"]] = [0,Date_SL]
        self.Date_ende_order = Date_SL
        self._postin =False
