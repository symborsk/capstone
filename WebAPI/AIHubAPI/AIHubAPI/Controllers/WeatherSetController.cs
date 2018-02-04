using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using AIHubAPI.Models;
using System.Data.Common;

namespace AIHubAPI.Controllers
{
    [Route("api/WeatherSetController")]
    public class WeatherSetController : Controller
    {
        private readonly AIHubContext _context;

        public WeatherSetController(AIHubContext context)
        {
            _context = context;
        }

        [HttpGet("GetAllForStation")]
        public IEnumerable<WeatherSet> GetAll()
        {
            return _context.WeatherSet.ToList();
        }

        [HttpGet("GetSetForStationDateRange")]
        public IActionResult GetWeatherDataByStationID(int id, DateTime startTime, DateTime endTime)
        {
            var item = _context.WeatherSet.FirstOrDefault(t => t.StationId == id);
            if (item == null)
            {
                return NotFound();
            }

            return new ObjectResult(item);
        }

        [HttpPost]
        public IActionResult InsertWeatherSet([FromBody] WeatherSet set)
        {
            return CreatedAtRoute("GetWeatherDataByID", new { id = set.StationId }, set);
        }
    }
}
