using System;
using System.Collections.Generic;
using System.Net;
using System.Web.Mvc;
using System.Threading.Tasks;

namespace AIHubWeb.Controllers
{
    public class HomeController : Controller
    {
        AzureStorageController restController = new AzureStorageController();
        AzureIotHubController messageController = new AzureIotHubController();

        public async Task<ActionResult> Index()
        {
            await restController.RefreshWeatherSets(WeatherSet.WeatherSetDateRanges.AllTime);
            ViewBag.WeatherStations = await restController.GetCurrentWeatherSets();
            return View();
        }

        public ActionResult About()
        {
            ViewBag.Message = "View data from the AI Hub Weatherstation.";

            return View();
        }

        [HttpGet]
        public async Task<ActionResult> GetWeatherSetsForNameAndRange(string statName, string startDate, string endDate)
        {
            DateTime start = DateTime.Parse(startDate);
            //We want the end of the day so add one second short of full day
            DateTime end = DateTime.Parse(endDate).Date.AddHours(23).AddMinutes(59).AddSeconds(59); ;

            List<WeatherSet> sets = await restController.GetStationListForName(statName, start, end);
            return Json(sets, JsonRequestBehavior.AllowGet);
        }

        [HttpGet]
        public async Task<ActionResult> GetConfigSetForStation(String statName)
        {
            StationOptions opt =  await restController.GetConfigSetting(statName);
           return Json(opt, JsonRequestBehavior.AllowGet);
        }

        [HttpPost]
        public async Task<ActionResult> UpdateConfigSetting(StationOptions opt)
        {
            if (opt == null)
            {
                return Json(new HttpStatusCodeResult(HttpStatusCode.BadRequest, "Not a valid option"));
            }
            else
            {
                bool succ  = await restController.UpdateDeviceConfigSettings(opt);
                bool succIot = await messageController.UpdateDeviceOptions(opt);

                if (succ)
                {
                    return Json(new HttpStatusCodeResult(HttpStatusCode.Accepted, "Success Updating"));
                }
                else
                {
                    return Json(new HttpStatusCodeResult(HttpStatusCode.InternalServerError, "Failure to contact server"));
                }
            }
        }

    }
}