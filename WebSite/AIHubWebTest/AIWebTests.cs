
/**
 * AIWebTest.cs
 * By: John Symborski
 * Capstone Group 2
 * UI automated tests ran with selenium
 * */


using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Interactions;
using OpenQA.Selenium.Firefox;

namespace AIHubWebTest
{
    [TestClass]
    public class AIWebTests
    {
        private const string websiteLink = "http://localhost/";

        [TestMethod]
        public void WebLaunch()
        {
            using (var driver = new ChromeDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                Assert.IsNotNull(driver.FindElementByClassName("container"));
            }

            using (var driver = new FirefoxDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                Assert.IsNotNull(driver.FindElementByClassName("container"));
            }
        }

        [TestMethod]
        public void MapLoad()
        {
            using (var driver = new ChromeDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                var mapGrid = driver.FindElementById("map_canvas");

                Assert.IsNotNull(mapGrid);
            }

            using (var driver = new FirefoxDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                var mapGrid = driver.FindElementById("map_canvas");

                Assert.IsNotNull(mapGrid);
            }
        }

        [TestMethod]
        public void NavBarClick()
        {
            using (var driver = new ChromeDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                Actions action = new Actions(driver);
                action.Click(driver.FindElementByLinkText("About"));
                Assert.AreEqual(driver.Url, websiteLink + @"/Home/About/");

                action.Click(driver.FindElementByLinkText("Contact"));
                Assert.AreEqual(driver.Url, websiteLink + @"/Home/Contact/");
            }
            

            using (var driver = new FirefoxDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                Actions action = new Actions(driver);
                action.Click(driver.FindElementByLinkText("About"));
                Assert.AreEqual(driver.Url, websiteLink + @"/Home/About/");

                action.Click(driver.FindElementByLinkText("Contact"));
                Assert.AreEqual(driver.Url, websiteLink + @"/Home/Contact/");
            }
        }

    }
}
