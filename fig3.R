library("Hmisc")
library("Hmisc")

#pdf("fig3.pdf")

par(mar=c(5, 4, 4, 2) + 0.1)

RO = c(0.0166, 0.0203, 0.0235, 0.0308, 0.037, 0.0304)
RT = c(0.0159, 0.0236, 0.0339, 0.0471, 0.0546, 0.0389)
CO = c(0.0052, 0.027, 0.0391, 0.0442, 0.039, 0.0261)
CT = c(0.0783, 0.0429, 0.0439, 0.0408, 0.0232, 0.0062)

fake_reliable = c(0.05660377358490566, 0.1060377358490566, 0.16037735849056603, 0.25471698113207547, 0.2747169811320755, 0.14754716981132077)

fake_cheaters = c(0.013714285714285714, 0.06742857142857143, 0.2062857142857143, 0.37085714285714283, 0.256, 0.08571428571428572)

test = c(0,0,0,0,0,0)

total_dist = c(fake_reliable, fake_cheaters)

groupname = c(0,0,0,0,0,0,1,1,1,1,1,1)

bin = c("0","1","2","3","4","5","0","1","2","3","4","5")

data <- tapply(total_dist, list(groupname,bin), sum)


barplot(data,beside=T,col=c("olivedrab4","darkorange"),ylim=c(0,0.5)
        ,ylab="frequency",xlab="observable cooperation index")

for (i in 1:6) {
  
  arrows(3*(i-1)+1.5, total_dist[i]-RO[i],3*(i-1)+1.5, total_dist[i]+RO[i],lwd = 1,code=3,angle = 90,length = 0.05)
}

for (i in 1:6) {
  
  arrows(3*(i-1)+2.5, total_dist[i+6]-CO[i],3*(i-1)+2.5, total_dist[i+6]+CO[i],lwd = 1,code=3,angle = 90,length = 0.05)
}

legend("topright",c("reliable players","cheater players"),fill=c("olivedrab4","darkorange"),inset=0.05)





#dev.off()