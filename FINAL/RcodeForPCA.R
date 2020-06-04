##treatment PCA

treat.df <- read.csv("treatmentforPCA.csv",header = T)

View(treat.df)
treat.pca=prcomp(treat.df[,-1])
summary(treat.pca)
weigtss<-treat.pca$x
View(weigtss)
math<-treat.pca$rotation

View(math[,1:6])
