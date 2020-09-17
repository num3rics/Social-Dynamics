library("Hmisc")
library("Hmisc")

#pdf("fig3.pdf")

path = 'D:/PABLO/Documentos (2TB)/WORK IN PROGRESS D/20 nodos y 30 rondas/Histos/'

visible_reliable <- dir(path, pattern ="visibleR.txt")
Visible_cheaters <- dir(path, pattern ="visibleC.txt")

true_reliable <- dir(path, pattern ="trueR.txt")
true_cheaters <- dir(path, pattern ="trueC.txt")


par(mar=c(5, 4, 4, 2) + 0.1)

RO = c(0.0166, 0.0203, 0.0235, 0.0308, 0.037, 0.0304)
RT = c(0.0159, 0.0236, 0.0339, 0.0471, 0.0546, 0.0389)
CO = c(0.0052, 0.027, 0.0391, 0.0442, 0.039, 0.0261)
CT = c(0.0783, 0.0429, 0.0439, 0.0408, 0.0232, 0.0062)

for(i in 1:length(visible_reliable)){
  
  fake_reliable = scan(visible_reliable[i], sep=",", dec=".")
  fake_reliable = fake_reliable/50
  fake_cheaters = scan(Visible_cheaters[i], sep=",", dec=".")
  fake_cheaters = fake_cheaters/50
  
  test = c(0,0,0,0,0,0)
  
  total_dist = c(fake_reliable, fake_cheaters)
  
  groupname = c(0,0,0,0,0,0,1,1,1,1,1,1)
  
  bin = c("0","1","2","3","4","5","0","1","2","3","4","5")
  
  data <- tapply(total_dist, list(groupname,bin), sum)
  
  png(filename= paste("D:/PABLO/Documentos (2TB)/WORK IN PROGRESS D/20 nodos y 30 rondas/Histos/plot", visible_reliable[i], ".png", sep = " ", collapse = NULL))
  
  barplot(data,beside=T,col=c("olivedrab4","darkorange"),ylim=c(0,1),ylab="frequency",xlab="observable cooperation index")
  
  for (i in 1:6) {
    arrows(3*(i-1)+1.5, total_dist[i]-RO[i],3*(i-1)+1.5, total_dist[i]+RO[i],lwd = 1,code=3,angle = 90,length = 0.05)
  }
  
  for (i in 1:6) {
    arrows(3*(i-1)+2.5, total_dist[i+6]-CO[i],3*(i-1)+2.5, total_dist[i+6]+CO[i],lwd = 1,code=3,angle = 90,length = 0.05)
  }
  
  legend("topright",c("reliable players","cheater players"),fill=c("olivedrab4","darkorange"),inset=0.05)
  
  dev.off()
}


for(i in 1:length(true_reliable)){
  
  real_reliable = scan(true_reliable[i], sep=",", dec=".")
  real_reliable = real_reliable/50
  real_cheaters = scan(true_cheaters[i], sep=",", dec=".")
  real_cheaters = real_cheaters/50
  
  test = c(0,0,0,0,0,0)
  
  total_dist = c(real_reliable, real_cheaters)
  
  groupname = c(0,0,0,0,0,0,1,1,1,1,1,1)
  
  bin = c("0","1","2","3","4","5","0","1","2","3","4","5")
  
  data <- tapply(total_dist, list(groupname,bin), sum)
  
  png(filename= paste("D:/PABLO/Documentos (2TB)/WORK IN PROGRESS D/20 nodos y 30 rondas/Histos/plot", true_reliable[i], ".png", sep = " ", collapse = NULL))
  
  barplot(data,beside=T,col=c("olivedrab4","darkorange"),ylim=c(0,1),ylab="frequency",xlab="real cooperation index")
  
  for (i in 1:6) {
    arrows(3*(i-1)+1.5, total_dist[i]-RO[i],3*(i-1)+1.5, total_dist[i]+RO[i],lwd = 1,code=3,angle = 90,length = 0.05)
  }
  
  for (i in 1:6) {
    arrows(3*(i-1)+2.5, total_dist[i+6]-CO[i],3*(i-1)+2.5, total_dist[i+6]+CO[i],lwd = 1,code=3,angle = 90,length = 0.05)
  }
  
  legend("topright",c("reliable players","cheater players"),fill=c("olivedrab4","darkorange"),inset=0.05)
  
  dev.off()
}

#################################################