using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Threading.Tasks;

namespace AIHubWeb.Controllers
{
    public class HomeController : Controller
    {
        WeatherSetsController restController = new WeatherSetsController();

        public async Task<ActionResult> Index()
        {
            await restController.RefreshWeatherSets(WeatherSet.WeatherSetDateRanges.AllTime);
            ViewBag.WeatherStations =  await restController.GetCurrentWeatherSets();
            return View();
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";
            
            return View();
        }

        [HttpGet]
        public async Task<ActionResult> GetWeatherSetsForNameAndRange(string statName, string startDate, string endDate)
        {
            await restController.RefreshWeatherSets(WeatherSet.WeatherSetDateRanges.AllTime);

            DateTime start = DateTime.Parse(startDate);
            DateTime end = DateTime.Parse(endDate);
            List<WeatherSet> sets = await restController.GetStationListForName(statName, start, end);
            return Json(sets, JsonRequestBehavior.AllowGet); 
        }
    }
}