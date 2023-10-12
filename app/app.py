from PySide6 import QtWidgets
import sys
import currency_converter

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertisseur de devise")
        self.c = currency_converter.CurrencyConverter(fallback_on_missing_rate=True)
        self.setup_ui()
        self.set_default_values()
        self.setup_css()
        self.setup_connections()
        
    # Initialisation de l'interface utilisateur
    def setup_ui(self):
        self.layout=QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom=QtWidgets.QComboBox()
        self.spn_montant=QtWidgets.QSpinBox()
        self.cbb_devisesTo=QtWidgets.QComboBox()
        self.spn_montantConverti=QtWidgets.QSpinBox()
        self.btn_inverse = QtWidgets.QPushButton("Inverser devise")

        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverse)
    
    # Configuration des valeurs par défaut
    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")

        self.spn_montant.setRange(1, 1000000)
        self.spn_montantConverti.setRange(1, 1000000)
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)
    
    # Configuration des connexions entre signaux et slots
    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverse.clicked.connect(self.inverser_devise)

    # Configuration des styles CSS (commenté)
    def setup_css(self):
        '''
        self.setStyleSheet("""
        background-color: rgb(30, 30, 30);
        color : rgb(240, 240, 240);                 
        border:none;                  
        """)
        '''
    
    # Calcul de la conversion de devise
    def compute(self):
        montant=self.spn_montant.value()
        devise_from=self.cbb_devisesFrom.currentText()
        devise_to=self.cbb_devisesTo.currentText()

        try:
            resultat = self.c.convert(montant, devise_from, devise_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion n'a pas fonctionné.")
        else:    
           self.spn_montantConverti.setValue(resultat)
    
    # Inversion des devises
    def inverser_devise(self):
        devise_from=self.cbb_devisesFrom.currentText()
        devise_to=self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)

        self.compute()

# Configuration de l'application
app = QtWidgets.QApplication([])

win = App()
win.show()

sys.exit(app.exec())
