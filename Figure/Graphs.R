#Loading libraries.
library(magrittr)
library(dplyr) 
library(hrbrthemes)
library(ggplot2)
library(ggpubr)


#Loading dataset

df.PreyPredatorModel<-as.data.frame(read.csv("DataPreyPredator_propstep_0.01.txt"))

df.PreyPredatorModel_Prey<-df.PreyPredatorModel[,1:3]
df.PreyPredatorModel_Pred<-df.PreyPredatorModel[,c(1,2,4)]



#Creating graph with similar layout

#Creating predators graph
Predators_graph<-df.PreyPredatorModel_Pred%>%ggplot(aes(PercPrey.Ini, PercPred.Ini, fill= PercPred.Final)) + geom_tile()+theme_ipsum() + theme(legend.position="bottom")+scale_fill_gradient(low="black", high="white",name="Final proportion",limits=c(0,0.025),guide = guide_colourbar(barheight = 1,barwidth=40,title.position="bottom",title.hjust=0.5,title.theme=element_text(hjust = 1.25,size = 14)))+xlim(0,0.80)+ylim(0,0.80)+xlab("Initial preys")+ylab("Initial predators")+theme(axis.title.x = element_text( hjust = 0.5,size = 14),axis.title.y = element_text(hjust = 0.5,size = 14)
)
#Creating prey graph
Prey_graph<-df.PreyPredatorModel_Prey%>%ggplot(aes(PercPrey.Ini, PercPred.Ini, fill= PercPrey.Final)) + geom_tile()+theme_ipsum() + theme(legend.position="bottom")+scale_fill_gradient(low="black", high="white",name="Final proportion",limits=c(0,0.025),guide = guide_colourbar(barheight = 1,barwidth=40,title.position="bottom",title.hjust=0.5,title.theme=element_text( hjust = 1.25,size = 14)))+xlim(0,0.80)+ylim(0,0.80)+xlab("Initial preys")+ylab("Initial predators")+theme(axis.title.x = element_text( hjust = 0.5,size = 14),axis.title.y = element_text(hjust = 0.5,size = 14)
)

#Creating joint graph
ggarrange(Predators_graph,Prey_graph,labels=c("Predators","Preys"),common.legend=TRUE,legend = "bottom")
