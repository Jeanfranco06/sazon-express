package com.sazonexpress.promocion;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@SpringBootApplication
@EnableConfigurationProperties
public class PromocionServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(PromocionServiceApplication.class, args);
    }
}
