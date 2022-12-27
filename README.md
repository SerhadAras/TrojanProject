# TrojanProject
## Dit is het eindproject voor het vak EthicalHacking

## Hoe run je dit?
1. Je start de Trojan bij de target door python github-client.py uit te voeren op de machine van de slachtoffer
2. Op je eigen machine (aanvaller) start je de log.py script. 

  Als **optie 1** bij het loggen heb je de mogelijkheid alle files die bij de slachtoffer(s) vandaan komen te tonen
  
  Als **optie 2** bij het loggen heb je de mogelijkheid om de inhoud van de laatste file die van de slachtoffer vandaan komt te tonen, codeerd in BASE64.
  
  Als **optie 3** bij het loggen heb je de mogelijkheid om de inhoud van de laatste file te tonen in clear text in de terminal. De data wordt op een leesbare manier getoond a.d.h.v. de rich library.  
  
  Als **optie 4** bij het loggen heb je de mogelijkheid om per 10 seconden te controleren naar nieuwe binnekomende files van de slachtoffer. Wanneer er een nieuwe file binnenkomt dan krijg krijg je een melding dat er een nieuwe file is geplaatst in de repo die info bevat over de slachtoffer. Je krijgt dan ook meteen de mogelijkheid om deze nieuw binnenkomende data te tonen in de terminal. 
