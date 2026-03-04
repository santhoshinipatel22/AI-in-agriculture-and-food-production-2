const WeatherAdvisory = require('../models/WeatherAdvisory');
const logger = require('../utils/logger');
const axios = require('axios');

const weatherService = {
  async getWeatherAdvisory(latitude, longitude) {
    try {
      // Fetch from OpenWeatherMap API
      const response = await axios.get(
        `${process.env.WEATHER_API_ENDPOINT}/weather?lat=${latitude}&lon=${longitude}&appid=${process.env.OPENWEATHER_API_KEY}&units=metric`
      );

      const weatherData = {
        temperature: response.data.main.temp,
        humidity: response.data.main.humidity,
        windSpeed: response.data.wind.speed,
        rainfall: response.data.rain?.['1h'] || 0,
        cloudiness: response.data.clouds.all,
        condition: response.data.weather[0].main,
        lastUpdated: new Date(),
      };

      return weatherData;
    } catch (error) {
      logger.error('Get weather error:', error.message);
      throw error;
    }
  },

  async getForecast(latitude, longitude) {
    try {
      const response = await axios.get(
        `${process.env.WEATHER_API_ENDPOINT}/forecast?lat=${latitude}&lon=${longitude}&appid=${process.env.OPENWEATHER_API_KEY}&units=metric`
      );

      const forecast = response.data.list.map(item => ({
        date: new Date(item.dt * 1000),
        temperature: item.main.temp,
        humidity: item.main.humidity,
        rainfall: item.rain?.['3h'] || 0,
        windSpeed: item.wind.speed,
        condition: item.weather[0].main,
      }));

      return forecast;
    } catch (error) {
      logger.error('Get forecast error:', error.message);
      throw error;
    }
  },

  async generateAgriculturalAdvisory(weatherData, cropType) {
    try {
      const advisory = {
        sowingAdvisory: 'Optimal conditions for sowing rice. Moisture level sufficient.',
        pesticideSprayingAdvisory: 'Avoid spraying during high wind speeds. Best time is early morning.',
        harvestingAdvisory: 'Monitor for adequate drying. High humidity might affect grain quality.',
        irrigationAdvisory: {
          recommendedWater: 50,
          frequency: 'Every 3 days',
          timing: 'Early morning or late evening',
          crops: [cropType],
        },
        bestCropForSeason: ['Rice', 'Sugarcane', 'Jute'],
      };

      return advisory;
    } catch (error) {
      logger.error('Generate agricultural advisory error:', error.message);
      throw error;
    }
  },

  async getWeatherAlerts(latitude, longitude) {
    try {
      // Mock weather alerts
      const alerts = [];

      // Check for extreme conditions
      const weather = await this.getWeatherAdvisory(latitude, longitude);

      if (weather.temperature > 38) {
        alerts.push({
          type: 'heat',
          severity: 'high',
          message: 'High temperature alert. Increase irrigation frequency.',
          startDate: new Date(),
          endDate: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000),
        });
      }

      if (weather.rainfall > 50) {
        alerts.push({
          type: 'heavy_rain',
          severity: 'medium',
          message: 'Heavy rainfall expected. Ensure drainage systems are active.',
          startDate: new Date(),
          endDate: new Date(Date.now() + 24 * 60 * 60 * 1000),
        });
      }

      return alerts;
    } catch (error) {
      logger.error('Get weather alerts error:', error.message);
      throw error;
    }
  },
};

module.exports = weatherService;
