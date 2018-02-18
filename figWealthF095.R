library("Hmisc")

# Calcular la media de las 5 iteraciones
# Valores y variables
a1=c(20.5, 48.1, 66.1, 90.0, 116.5, 158.3, 198.3, 250.4, 298.9, 346.1, 384.0, 450.2, 511.1, 570.9, 632.8, 706.9, 789.8, 853.4, 902.2, 986.7, 1060.8, 1132.3, 1219.3, 1293.0, 1384.7, 1475.0, 1545.2, 1630.7, 1721.3, 1805.2)
a2=c(24.6, 56.5, 81.7, 126.2, 166.9, 216.6, 274.9, 342.3, 412.9, 498.6, 588.1, 670.8, 768.1, 861.4, 950.3, 1047.3, 1120.5, 1214.2, 1258.2, 1339.2, 1424.6, 1499.3, 1606.5, 1672.6, 1715.1, 1787.1, 1853.2, 1932.7, 1975.0, 2041.6)
a3=c(26.3, 53.8, 76.8, 123.2, 156.0, 196.1, 233.2, 273.6, 316.0, 348.7, 398.2, 433.4, 482.7, 508.3, 561.4, 595.6, 613.3, 653.8, 687.5, 735.5, 772.4, 798.5, 848.0, 877.3, 918.8, 962.0, 983.4, 1010.0, 1027.7, 1053.3)
a4=c(16.0, 35.3, 69.7, 107.0, 132.2, 171.1, 195.1, 232.5, 265.0, 312.0, 355.7, 416.3, 445.8, 485.1, 546.2, 590.6, 655.5, 703.3, 782.9, 840.5, 915.7, 964.8, 1023.0, 1100.3, 1162.3, 1246.4, 1316.7, 1381.6, 1458.0, 1525.3)
a5=c(22.6, 49.1, 79.9, 120.0, 166.4, 222.2, 260.1, 284.6, 351.5, 411.0, 449.5, 507.0, 584.6, 668.3, 744.5, 817.7, 882.9, 942.1, 1015.6, 1093.2, 1170.3, 1242.1, 1301.3, 1374.5, 1455.0, 1539.6, 1605.2, 1676.5, 1742.6, 1812.7)

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
wealth.names <- dir(path, pattern ="F_0.95_pagos.txt") #F_0.95_pagos.txt
wealthC.names <- dir(path, pattern ="F_0.95_pagosC.txt") #F_0.95_pagosC.txt
wealthR.names <- dir(path, pattern ="F_0.95_pagosR.txt") #F_0.95_pagosR.txt

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
  
  plot(x30, acum, col="blue", pch=15, xlim=c(0,30), ylim=c(0,3000), lwd=1, xlab="round", ylab="cummulated wealth")
  par(new=TRUE)
  plot(x30, acumC, col="darkorange", pch=17, xlim=c(0,30), ylim=c(0,3000), axes="FALSE", xlab="", ylab="")
  par(new=TRUE)
  plot(x30, acumR, col="olivedrab4", pch=18, xlim=c(0,30), ylim=c(0,3000), axes="FALSE", xlab="", ylab="")
  par(new=TRUE)
  plot(x30, RRtreat, col="black", pch=16, xlim=c(0,30), ylim=c(0,3000), axes="FALSE", xlab="", ylab="")
  
  title(main=wealth.names[j])
  legend("bottomright", legend = c("RR treatment","FR treatment","cheater players","reliable players"), bty="n", pch=c(16,15,17,18),lwd=c(2.5,2.5,2.5),col=c("black","blue","darkorange","olivedrab4"),inset=0.04,cex=1)
  
  dev.off()
}