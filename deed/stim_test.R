createGamble <- function(certain = FALSE, reduced = FALSE) {
  if (certain & reduced) {
    stop("Gamble cannot be both certain and reduced.")
  }

  # probabilities
  p11 <- round(runif(1, .05, .95), 2)
  if (certain) {
  	p21 <- 1
  } else {
    p21 <- round(runif(1, .05, .95), 2)
  }
  p12 <- 1 - p11
  p22 <- 1 - p21

  # values
  v11 <- round(runif(1, -100, 100), 1)
  v12 <- round(runif(1, -100, 100), 1)
  ev <- p11 * v11 + p12 * v12
  if (certain) {
  	v21 <- ev
  	v22 <- 0
  } else {
  	if (reduced) {
      v21 <- 0
  } else {
      v21 <- round(runif(1, -100, 100), 1)
    }
    v22 <- round((ev - p21 * v21) / p22, 1)
  }
  if (v22 < 0) {
  	return(createGamble(certain, reduced))
  }

  # format
  # reshape2::melt(list(DistA = matrix(c(v11, v12, p11, p12), ncol = 2), DistB = matrix(c(v21, v22, p21, p22), ncol = 2)))
  data.frame(v11 = v11,
             v12 = v12,
             v21 = v21,
             v22 = v22,
             p11 = p11,
             p12 = p12,
             p21 = p21,
             p22 = p22,
             certain = certain,
             reduced = reduced)
}

gamblePay <- function() {
  cert <- rbinom(1, 1, .5)
  red <- ifelse(cert, 0, rbinom(1, 1, .5))
  a <- createGamble(cert, red)
  p <- sample(c(a$v11, a$v12, a$v21, a$v22), 1, prob = c(a$p11, a$p12, a$p21, a$p22))
  v <- p / abs(p)
  ifelse(is.na(v), 0, v * log(abs(p)) / 10)
}

nocens <- replicate(10000, replicate(3, gamblePay()))
mean(ifelse(nocens > 0, nocens, 0))
mean(nocens[nocens > 0])