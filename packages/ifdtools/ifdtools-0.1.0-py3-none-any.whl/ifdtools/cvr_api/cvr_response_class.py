from dataclasses import dataclass

@dataclass
class CVRResponse:
    """Klasse som håndteret et respons fra CVR
    
    NB! Det antages at der tages udgangspunkt i det fulde response - altså uden selektering i output via query."""
    response: dict
    
    def __post_init__(self):
        if self.__invalid_input():
            raise TypeError("response er ikke en dict med det forventede format")
        self.__resp_type = self.__extract_resp_type()
        self.__meta_data = self.__extract_meta_data()
    
    def __invalid_input(self) -> bool:
        """Udestår"""
        return False
    
    def __extract_resp_type(self) -> str:
        """Udleder hvorvidt reponse er på cvr- eller p-nummer."""
        if self.response["_source"].get("Vrvirksomhed"):
            return "cvr"
        else:
            return "pnr"
        
    def __extract_meta_data(self) -> dict:
        if self.__resp_type == "cvr":
            return self.response["_source"]["Vrvirksomhed"]["virksomhedMetadata"]
        else:
            return self.response["_source"]["VrproduktionsEnhed"]["produktionsEnhedMetadata"]
        
    @property
    def get_all(self) -> dict:
        return {
            "cvr": self.cvr,
            "cvr_str": str(self.cvr),
            "name": self.name,
            "h_branche": self.hbranche,
            "status": self.status,
            "ant_ansatte": self.ant_ansatte,
            "ant_aarsvaerk": self.ant_aarsvaerk,
            "ant_ansatte_yyyymm": self.ant_ansatte_yyyymm,
        }
        
    @property
    def cvr(self) -> int:
        if self.__resp_type == "cvr":
            return self.response["_source"]["Vrvirksomhed"]["cvrNummer"]
        else:
            try:
                return self.response["_source"]["VrproduktionsEnhed"]["virksomhedsrelation"][0]["cvrNummer"]
            except IndexError:
                return None
    
    @property
    def hbranche(self) -> int:
        return self.__meta_data["nyesteHovedbranche"]["branchekode"] 

    @property
    def name(self) -> str:
        return self.__meta_data["nyesteNavn"]["navn"]
        
    @property
    def status(self) -> str:
        return self.__meta_data["sammensatStatus"]
        
    @property
    def ant_ansatte(self) -> int:
        try: 
            return self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]["antalAnsatte"]
        except TypeError:
            return None

    @property
    def ant_aarsvaerk(self) -> int:
        try: 
            return self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]["antalAarsvaerk"]
        except TypeError:
            return None

    @property
    def ant_ansatte_yyyymm(self) -> int:
        try:
            aar = self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]["aar"]
            mdr = self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]["maaned"]
            result = f"{(aar*100)+mdr:02d}"
            return int(result)
        except TypeError:
            return None
