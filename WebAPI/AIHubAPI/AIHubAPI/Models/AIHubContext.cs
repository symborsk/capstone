using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace AIHubAPI.Models
{
    public class AIHubContext : DbContext
    {
        public AIHubContext(DbContextOptions<AIHubContext> options)
            : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<WeatherSet>()
                .HasKey(c => new { c.StationId, c.RecordedTime });
        }

        public DbSet<WeatherSet> WeatherSet { get; set; }
    }
}
