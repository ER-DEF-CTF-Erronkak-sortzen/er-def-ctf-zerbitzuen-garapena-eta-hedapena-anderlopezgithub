FROM php:7.4-apache

# Install necessary extensions for MariaDB
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Copy the source code to the container
COPY src/ /var/www/html/

# Set the working directory
WORKDIR /var/www/html/