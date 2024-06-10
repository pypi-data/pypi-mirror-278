
class mateoperaciones:
    """
    Esta es una clase que le ingresan números enteros

    a = número entero
    b= número entero diferente de cero
    """

    def __init__(self,a,b):
        self.a=a
        self.b=b

    
    def suma(self):
        """

        this is the method to sum two values 
        """
        return self.a+self.b

    def resta(self):
        return self.a-self.b
    
    def multipicacion(self):
        return self.a*self.b
    
    def division(self):
        return self.a/self.b