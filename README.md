# SSO_2022_Eye_Tracking

Projekat iz predmeta 13E053SSO na ETF UB, školska 2021/2022.

Pokreti očiju snimani su Tobii Eye Tracker sistemom, i tako su generisani podaci o koordinatama pogleda tri ispitanika za dva različita seta stimulusa. U ovom repozitorijumu se nalaze implementacije dva algoritma koja služe za izdvajanje sakada i fiksacija na osnovu koordinata tačaka pogleda.

Prvi algoritam, IDT, generiše klastere fiksacija na osnovu njihove maksimalne disperzije i minimalnog trajanja. Tačka se dodaje klasteru ukoliko ne povećava njegovu disperziju iznad maksimalne. Klaster mora imati barem minimalno trajanje da bi bio formiran.

Drugi algoritam, IMST, generiše klastere fiksacija na osnovu minimalnog stabla (MST) tačaka pogleda. Grana u MST se preseca ukoliko je dovoljno duža od svojih lokalnih suseda i prelazi standardnu devijaciju dužine, čime se od jednog klastera stvaraju dva.

Autori rada su studenti ETF:
Dušan Cvijetić, Iva Marković i Minja Vuković.

Mentor je:
dr Milica Janković, vanredni profesor.
