/***
 * AIHubContext.cs
 * File by: John Symborski 
 * Capstone Group 2
*  This class basically represents a database in entity framework
*  You have dbset to represent  our table and any configuration can be added when creating
*  the model if the database is overly complex
 * */

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
            //Composite Key
            modelBuilder.Entity<WeatherSet>()
                .HasKey(c => new { c.StationId, c.RecordedTime });
        }

        public DbSet<WeatherSet> WeatherSet { get; set; }
    }
}
