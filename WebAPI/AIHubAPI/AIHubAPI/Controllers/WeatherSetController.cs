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

        [HttpGet]
        public IEnumerable<WeatherSet> GetAll()
        {
            return _context.WeatherSet.ToList();
        }

        // GET api/values
        //[Route("~/api/WeatherSetController/GetWeatherDataByStationID/{id}")]
        [HttpGet("{id}", Name = "GetWeatherDataByID")]
        public IActionResult GetWeatherDataByStationID(int id)
        {
            var item = _context.WeatherSet.FirstOrDefault(t => t.StationId == id);
            if (item == null)
            {
                return NotFound();
            }

            return new ObjectResult(item);
        }

        //// GET api/values/5
        //[HttpGet("{id}")]
        //public string Get(int id)
        //{
        //    return "value";
        //}

        //// POST api/values
        //[HttpPost]
        //public void Post([FromBody]string value)
        //{
        //}

        //// PUT api/values/5
        //[HttpPut("{id}")]
        //public void Put(int id, [FromBody]string value)
        //{
        //}

        //// DELETE api/values/5
        //[HttpDelete("{id}")]
        //public void Delete(int id)
        //{
        //}
    }
}
