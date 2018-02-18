#pdf("fig2.pdf")

path = 'D:/PABLO/Documentos (2TB)/WORK IN PROGRESS D/20 nodos y 30 rondas/Scatters/'

puntos.names <- dir(path, pattern ="puntos.txt")
porcentajes.names <- dir(path, pattern ="porcentaje.txt")

for(i in 1:length(puntos.names)){
  # Cooperacion individual por ronda (normalizada sobre 5)
  coop = scan(porcentajes.names[i], sep=",", dec=".")
  
  # Puntos comprados por ronda
  cost = scan(puntos.names[i], sep=",", dec=".")
  
  png(filename= paste("D:/PABLO/Documentos (2TB)/WORK IN PROGRESS D/20 nodos y 30 rondas/Scatters/plot", puntos.names[i], ".png", sep = " ", collapse = NULL))
  
  plot(cost, coop,log="",pch=20,col="black",xlim=c(0,5),ylim=c(0,1),lwd=0.5,xlab="points purchased per round",ylab="individual cooperation frequency")
  
  segments(0, 1, 5, 0, lwd=2, lty=3)
  
  segments(0.5, 0, 0.5, 1, col="purple", lwd=2)
  
  dev.off()
}