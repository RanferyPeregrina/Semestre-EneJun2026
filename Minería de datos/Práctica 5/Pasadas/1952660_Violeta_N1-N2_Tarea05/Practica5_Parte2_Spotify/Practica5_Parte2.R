library(cluster)
library(factoextra)
library(tidyverse)
# Cargar dataset original
datos_original <- read.csv("spotifydataset.csv")

View(datos_original)
str(datos_original)
colnames(datos_original)

# Filtrar canciones latinas
datos_latinos <- datos_original %>%
  filter(grepl("latin|reggaeton|bachata|urbano|tropical|mexican", genres, ignore.case = TRUE))

View(datos_latinos)
nrow(datos_latinos)

# Tomar muestra de 50 canciones
set.seed(123)

datos_latinos_50 <- datos_latinos %>%
  sample_n(50)

View(datos_latinos_50)

# Guardar nuevo dataset pequeño
write.csv(datos_latinos_50, "spotify_latinos_50.csv", row.names = FALSE)

# Cargar el nuevo dataset
datos <- read.csv("spotify_latinos_50.csv")

View(datos)
str(datos)
colnames(datos)

# Seleccionar variables numéricas para clustering
datos_num <- datos %>%
  select(duration_ms, track_popularity, danceability, energy, key, loudness,
         speechiness, acousticness, instrumentalness, liveness, valence, tempo)

View(datos_num)
summary(datos_num)

# Escalar datos
datos_scaled <- scale(datos_num)
View(datos_scaled)

# Método del codo / WSS
fviz_nbclust(datos_scaled, kmeans, method = "wss")

# Método Silhouette
fviz_nbclust(datos_scaled, kmeans, method = "silhouette")

# Gap Statistic
gap_stat <- clusGap(datos_scaled, FUN = kmeans, nstart = 25, K.max = 10, B = 50)
fviz_gap_stat(gap_stat)

# K-means con 3 clústeres
set.seed(123)
km <- kmeans(datos_scaled, centers = 3, nstart = 25)
fviz_cluster(km, data = datos_scaled)
km

# PAM con 3 clústeres
pam_res <- pam(datos_scaled, k = 3)
fviz_cluster(pam_res, data = datos_scaled)
pam_res

# CLARA con 3 clústeres
clara_res <- clara(datos_scaled, k = 3)
fviz_cluster(clara_res, data = datos_scaled)
clara_res

# Agregar clústeres al dataset
datos$cluster_kmeans <- km$cluster
datos$cluster_pam <- pam_res$clustering
datos$cluster_clara <- clara_res$clustering
View(datos)

# Guardar archivo final con clústeres
write.csv(datos, "spotify_latinos_clustering.csv", row.names = FALSE)