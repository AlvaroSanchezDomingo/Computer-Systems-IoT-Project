"use strict";

const logger = require("../utils/logger");
const accounts = require("./accounts.js");
const uuid = require("uuid");
const axios = require('axios')

const dashboard = {
  index(request, response) {
    logger.info("dashboard rendering");
    const loggedInUser = accounts.getCurrentUser(request);

    const milliseconds = 100;
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);

    axios.get('http://blynk-cloud.com/c3bUKILDyi0R_dXa4hr3el77KoLYW49b/project')
      .then(resp => {
        console.log(resp.data);
        const value0 = parseInt(resp.data.widgets[0].value);
        const value1 = resp.data.widgets[1].value;
        const value2 = resp.data.widgets[2].value;
        const value3 = resp.data.widgets[3].value;

        const viewData = {
          relay : value0,
          temperature : value1,
          humidity : value2,
          light : value3

        };
        response.render("dashboard", viewData);
      })
      .catch(err => {
         //Handle Error Here
        console.error(err);
        response.render("dashboard", viewData);
    });

  },
  toggle0(request, response){
    axios.get('http://blynk-cloud.com/c3bUKILDyi0R_dXa4hr3el77KoLYW49b/get/v0')
      .then(resp => {
        console.log(resp.data);
        const value0 = parseInt(resp.data[0]);

        if(value0 === 0){
          axios.get('http://blynk-cloud.com/c3bUKILDyi0R_dXa4hr3el77KoLYW49b/update/V0?value=1')
        }else{
          axios.get('http://blynk-cloud.com/c3bUKILDyi0R_dXa4hr3el77KoLYW49b/update/V0?value=0')
        }

        response.redirect('/dashboard/');

      })
      .catch(err => {
        //Handle Error Here
        console.error(err);
        response.redirect('/dashboard/');
      });

  }



};

module.exports = dashboard;
