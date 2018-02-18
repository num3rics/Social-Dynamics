library("Hmisc")

# Calcular la media de las 5 iteraciones
# Valores y variables
a1=c(17.699999999999999, 45.799999999999997, 77.799999999999997, 117.59999999999999, 159.19999999999999, 201.90000000000001, 246.5, 287.19999999999999, 341.69999999999999, 388.80000000000001, 430.30000000000001, 479.10000000000002, 517.70000000000005, 577.29999999999995, 623.70000000000005, 671.79999999999995, 743.10000000000002, 815.39999999999998, 888.10000000000002, 906.29999999999995, 967.60000000000002, 1054.5999999999999, 1079.0, 1129.5, 1172.5, 1224.0, 1257.7, 1282.8, 1339.0999999999999, 1357.8)
a2=c(18.399999999999999, 47.200000000000003, 70.299999999999997, 108.90000000000001, 138.69999999999999, 177.5, 217.0, 272.19999999999999, 314.19999999999999, 362.30000000000001, 430.80000000000001, 486.69999999999999, 546.5, 622.20000000000005, 693.39999999999998, 764.0, 814.79999999999995, 866.79999999999995, 932.89999999999998, 990.89999999999998, 1052.9000000000001, 1092.9000000000001, 1169.8, 1226.3, 1292.0999999999999, 1357.7, 1408.2, 1481.0, 1542.0, 1605.9000000000001)
a3=c(25.100000000000001, 48.799999999999997, 66.400000000000006, 106.40000000000001, 140.19999999999999, 182.0, 238.80000000000001, 282.89999999999998, 329.30000000000001, 373.0, 439.60000000000002, 528.0, 612.20000000000005, 685.5, 751.10000000000002, 827.0, 917.39999999999998, 1015.6, 1114.5, 1194.0999999999999, 1280.9000000000001, 1355.5999999999999, 1436.5999999999999, 1495.3, 1555.0, 1614.2, 1657.2, 1714.9000000000001, 1770.9000000000001, 1813.4000000000001)
a4=c(28.399999999999999, 59.399999999999999, 108.5, 157.80000000000001, 217.0, 287.80000000000001, 364.5, 451.60000000000002, 529.89999999999998, 641.29999999999995, 736.39999999999998, 844.0, 957.20000000000005, 1056.8, 1171.4000000000001, 1270.5, 1369.2, 1484.5, 1577.0, 1670.5, 1769.5999999999999, 1874.5999999999999, 1956.0999999999999, 2044.0999999999999, 2130.1999999999998, 2195.8000000000002, 2255.0, 2335.0, 2385.3000000000002, 2447.6999999999998)
a5=c(32.600000000000001, 81.5, 138.69999999999999, 200.59999999999999, 265.19999999999999, 342.39999999999998, 427.10000000000002, 524.20000000000005, 602.20000000000005, 689.89999999999998, 791.70000000000005, 877.0, 954.20000000000005, 1003.8, 1076.8, 1150.3, 1246.4000000000001, 1296.0, 1362.4000000000001, 1428.8, 1503.0, 1576.3, 1650.5, 1708.5, 1787.4000000000001, 1887.0, 1947.2, 1974.8, 2040.7, 2098.4000000000001)

errorsdRR <- numeric(30)

# Media
a = a1+a2+a3+a4+a5;
a = a/5

# Error estandar
A = matrix(c(a1,a2,a3,a4,a5), nrow=5, ncol=30, byrow = TRUE)
for(i in 1:5){errorsdRR <- (colMeans(A)-A[i,])^2+errorsdRR}
errorsdRR <- sqrt(errorsdRR)/(sqrt(5))

# Calcular figuras
#pdf("fig4.pdf")

# Ruta archivos
path = 'D:/PABLO/Documentos (2TB)/WORK IN PROGRESS D/20 nodos y 30 rondas/Wealth/'

# Patrones para leer
wealth.names <- dir(path, pattern ="F_1.00_pagos.txt") #F_1.00_pagos.txt
wealthC.names <- dir(path, pattern ="F_1.00_pagosC.txt") #F_1.00_pagosC.txt
wealthR.names <- dir(path, pattern ="F_1.00_pagosR.txt") #F_1.00_pagosR.txt

# Medias del RR
RRtreat<-a

# Rondas
x30 <- 1:30
# Numero de programas
numprog <- 5
# Acumuladores
acum <- numeric(30)
acumC <- numeric(30)
acumR <- numeric(30)
errorsd <- numeric(30)
errorsdC <- numeric(30)
errorsdR <- numeric(30)
Bacum <- matrix(0, nrow = 5, ncol = 30)
BacumC <- matrix(0, nrow = 5, ncol = 30)
BacumR <- matrix(0, nrow = 5, ncol = 30)


# Bucles
for(j in 1:length(wealth.names)){
  # bucle para la media
  for(i in 1:numprog){
    inicio <- 30*(i-1)+1
    fin <- 30*(i-1)+30
    wealth <- scan(wealth.names[j], sep=",", dec=".") # wealth.names[j]
    Bacum[i,] <- wealth[inicio:fin]
    wealthC <- scan(wealthC.names[j], sep=",", dec=".") # wealthC.names[j]
    BacumC[i,] <- wealthC[inicio:fin]
    wealthR <- scan(wealthR.names[j], sep=",", dec=".") # wealthR.names[j]
    BacumR[i,] <- wealthR[inicio:fin]
  } # ya tengo una matriz donde cada fila es una iteracion y cada columna una ronda
  
  # saco la media de las iteraciones
  acum <- colMeans(Bacum)
  acumC <- colMeans(BacumC)
  acumR <- colMeans(BacumR)
  
  # bucle para el error estandar
  for(i in 1:numprog){
    errorsd <- (colMeans(Bacum)-Bacum[i,])^2+errorsd
    errorsdC <- (colMeans(BacumC)-BacumC[i,])^2+errorsdC
    errorsdR <- (colMeans(BacumR)-BacumR[i,])^2+errorsdR
  } # ya tengo tres vectores donde cada entrada es la varianza de las 5 iteraciones
  
  # saco el error estandar
  errorsd <- sqrt(errorsd)/(sqrt(numprog))
  errorsdC <- sqrt(errorsdC)/(sqrt(numprog))
  errorsdR <- sqrt(errorsdR)/(sqrt(numprog))
  
  # grafico
  png(filename= paste("D:/PABLO/Documentos (2TB)/WORK IN PROGRESS D/20 nodos y 30 rondas/Wealth/plot", wealth.names[j], ".png", sep = " ", collapse = NULL))
  
  par(mar=rep(5,4))
  
  plot(x30, acum, col="blue", pch=15, xlim=c(0,30), ylim=c(0,3000), lwd=0.5, xlab="round", ylab="cummulated wealth")
  par(new=TRUE)
  plot(x30, acumC, col="darkorange", pch=17, xlim=c(0,30), ylim=c(0,3000), axes="FALSE", xlab="", ylab="")
  par(new=TRUE)
  plot(x30, acumR, col="olivedrab4", pch=18, xlim=c(0,30), ylim=c(0,3000), axes="FALSE", xlab="", ylab="")
  par(new=TRUE)
  plot(x30, RRtreat, col="black", pch=16, xlim=c(0,30), ylim=c(0,3000), axes="FALSE", xlab="", ylab="")
  
  legend("bottomright", legend = c("RR treatment","FR treatment","cheater players", "reliable players"), bty="n", pch=c(16,15,17,18),lwd=c(2.5,2.5,2.5),col=c("black","blue","darkorange","olivedrab4"),inset=0.04,cex=1)
  
  dev.off()
}