library(cluster)
library(factoextra)
library(tidyverse)

datos <- read.csv(file.choose(), header = TRUE)


rownames(datos) <- datos[, 1]
datos <- datos[, -1]


datos_norm <- scale(datos)

fviz_nbclust(datos_norm, kmeans, method = "silhouette") +
  labs(title = "Número óptimo de clusters (K-means - Silhouette)")

fviz_nbclust(datos_norm, kmeans, method = "wss") +
  labs(title = "Número óptimo de clusters (K-means - Elbow)")


gap_stat <- clusGap(datos_norm, FUN = kmeans, nstart = 25, K.max = 10, B = 50)
fviz_gap_stat(gap_stat) +
  labs(title = "Número óptimo de clusters (Gap Statistic)")


km_res <- kmeans(datos_norm, centers = 3, nstart = 25)


fviz_cluster(km_res, data = datos_norm,
             ellipse.type = "convex",
             palette = "jco",
             ggtheme = theme_minimal())


fviz_nbclust(datos_norm, pam, method = "silhouette") +
  labs(title = "Número óptimo de clusters (PAM)")

pam_res <- pam(datos_norm, k = 3)

fviz_cluster(pam_res, data = datos_norm,
             ellipse.type = "t",
             palette = "jco",
             ggtheme = theme_minimal())


clara_res <- clara(datos_norm, k = 3, samples = 50, pamLike = TRUE)


fviz_cluster(clara_res, data = datos_norm,
             ellipse.type = "norm",
             palette = "jco",
             ggtheme = theme_minimal()) +
  labs(title = "Clustering CLARA")


datos_clasificados <- datos %>%
  mutate(Cluster_KMeans = km_res$cluster,
         Cluster_PAM = pam_res$clustering,
         Cluster_CLARA = clara_res$clustering)


head(datos_clasificados)


write.csv(datos_clasificados, "datos_clasificados_completo.csv", row.names = TRUE)
