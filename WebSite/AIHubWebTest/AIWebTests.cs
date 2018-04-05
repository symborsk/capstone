
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
                driver.FindElementByLinkText("About").Click();;
                var aboutTitle = driver.FindElementById("AboutTitle");

                Assert.IsNotNull(aboutTitle);
            }
            

            using (var driver = new FirefoxDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                driver.FindElementByLinkText("About").Click(); ;
                var aboutTitle = driver.FindElementById("AboutTitle");

                Assert.IsNotNull(aboutTitle);
            }
        }

        [TestMethod]
        public void DownloadTestSets()
        {
            using (var driver = new ChromeDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                System.Threading.Thread.Sleep(2000);

                //Click the google map marker
                driver.FindElementByCssSelector("div[title='thor']").Click();

                System.Threading.Thread.Sleep(2000);

                //Click the View Details
                driver.FindElementByCssSelector("button[onclick^=DisplayStationDataTable]").Click();      //Click the result range

                System.Threading.Thread.Sleep(2000);

                //Click the results
                driver.FindElementById("resultrange").Click();

                System.Threading.Thread.Sleep(2000);

                //Click the all time filter
                driver.FindElementByCssSelector("li[data-range-key=\"All Time\"]").Click();

                System.Threading.Thread.Sleep(2000);

                //Gather all the elements that are are in the results table
                var test = driver.FindElementsByCssSelector("table[id=resultsTable] tbody > tr");

                //ensure 2 data sets are gotten
                Assert.AreEqual(2, test.Count, "Wrong number of data sets returned");

                //These are our expected values for this specific test set
                Assert.AreEqual("1/3/2018, 11:00:00 PM 14.4 24.1 Southeast 3.491153 0.000000 2.880000 --- ---", test[0].Text, "Incorrect values return for first data set");
                Assert.AreEqual("1/3/2018, 5:00:00 PM 10.5 15 West 51.862736 0.000000 0.000000 --- ---", test[1].Text, "Incorrect values return for second data set");
            }

            using (var driver = new FirefoxDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                System.Threading.Thread.Sleep(2000);

                //Click the google map marker
                driver.FindElementByCssSelector("div[title='thor']").Click();

                System.Threading.Thread.Sleep(2000);

                //Click the View Details
                driver.FindElementByCssSelector("button[onclick^=DisplayStationDataTable]").Click();      //Click the result range

                System.Threading.Thread.Sleep(2000);

                //Click the results
                driver.FindElementById("resultrange").Click();

                System.Threading.Thread.Sleep(2000);

                //Click the all time filter
                driver.FindElementByCssSelector("li[data-range-key=\"All Time\"]").Click();

                System.Threading.Thread.Sleep(2000);

                //Gather all the elements that are are in the results table
                var test = driver.FindElementsByCssSelector("table[id=resultsTable] tbody > tr");

                System.Threading.Thread.Sleep(2000);

                //ensure 2 data sets are gotten
                Assert.AreEqual(2, test.Count, "Wrong number of data sets returned");

                //These are our expected values for this specific test set
                Assert.AreEqual("1/3/2018, 11:00:00 PM 14.4 24.1 Southeast 3.491153 0.000000 2.880000 --- ---", test[0].Text, "Incorrect values return for first data set");
                Assert.AreEqual("1/3/2018, 5:00:00 PM 10.5 15 West 51.862736 0.000000 0.000000 --- ---", test[1].Text, "Incorrect values return for second data set");
            }

        }

        [TestMethod]
        public void DownloadSpecificRangeSuccess()
        {
            using (var driver = new ChromeDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                System.Threading.Thread.Sleep(2000);

                //Click the google map marker
                driver.FindElementByCssSelector("div[title='thor']").Click();

                System.Threading.Thread.Sleep(2000);

                //Click the View Details
                driver.FindElementByCssSelector("button[onclick^=DisplayStationDataTable]").Click();      //Click the result range

                System.Threading.Thread.Sleep(2000);

                //Click the results
                driver.FindElementById("resultrange").Click();

                System.Threading.Thread.Sleep(2000);

                //Select a valid range
                driver.FindElementByCssSelector("li[data-range-key=\"Custom Range\"]").Click();
                driver.FindElementByCssSelector("input[name=daterangepicker_start]").Clear();
                driver.FindElementByCssSelector("input[name=daterangepicker_start]").SendKeys(@"01/03/2018");
                driver.FindElementByCssSelector("input[name=daterangepicker_end]").Clear();
                driver.FindElementByCssSelector("input[name=daterangepicker_end]").SendKeys(@"01/03/2018");
                driver.FindElementByCssSelector("button[class^=applyBtn").Click();

                System.Threading.Thread.Sleep(2000);

                //Gather all the elements that are are in the results table
                var test = driver.FindElementsByCssSelector("table[id=resultsTable] tbody > tr");

                //ensure 2 data sets are gotten
                Assert.AreEqual(2, test.Count, "Wrong number of data sets returned");
            }

            using (var driver = new FirefoxDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                System.Threading.Thread.Sleep(2000);

                //Click the google map marker
                driver.FindElementByCssSelector("div[title='thor']").Click();

                System.Threading.Thread.Sleep(2000);

                //Click the View Details
                driver.FindElementByCssSelector("button[onclick^=DisplayStationDataTable]").Click();      //Click the result range

                System.Threading.Thread.Sleep(2000);

                //Click the results
                driver.FindElementById("resultrange").Click();

                System.Threading.Thread.Sleep(2000);

                //Select a valid range
                driver.FindElementByCssSelector("li[data-range-key=\"Custom Range\"]").Click();
                driver.FindElementByCssSelector("input[name=daterangepicker_start]").Clear();
                driver.FindElementByCssSelector("input[name=daterangepicker_start]").SendKeys(@"01/03/2018");
                driver.FindElementByCssSelector("input[name=daterangepicker_end]").Clear();
                driver.FindElementByCssSelector("input[name=daterangepicker_end]").SendKeys(@"01/03/2018");
                driver.FindElementByCssSelector("button[class^=applyBtn").Click();

                System.Threading.Thread.Sleep(2000);

                //Gather all the elements that are are in the results table
                var test = driver.FindElementsByCssSelector("table[id=resultsTable] tbody > tr");

                //ensure 2 data sets are gotten
                Assert.AreEqual(2, test.Count, "Wrong number of data sets returned");
            }
        }

        [TestMethod]
        public void DownloadSpecificRangeFailure()
        {
            using (var driver = new ChromeDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                System.Threading.Thread.Sleep(2000);

                //Click the google map marker
                driver.FindElementByCssSelector("div[title='thor']").Click();

                System.Threading.Thread.Sleep(2000);

                System.Threading.Thread.Sleep(2000);

                //Click the View Details
                driver.FindElementByCssSelector("button[onclick^=DisplayStationDataTable]").Click();      //Click the result range

                System.Threading.Thread.Sleep(2000);

                //Click the results
                driver.FindElementById("resultrange").Click();

                System.Threading.Thread.Sleep(2000); ;

                //Select a valid range
                driver.FindElementByCssSelector("li[data-range-key=\"Custom Range\"]").Click();
                driver.FindElementByCssSelector("input[name=daterangepicker_start]").Clear();
                driver.FindElementByCssSelector("input[name=daterangepicker_start]").SendKeys(@"01/04/2018");
                driver.FindElementByCssSelector("input[name=daterangepicker_end]").Clear();
                driver.FindElementByCssSelector("input[name=daterangepicker_end]").SendKeys(@"01/04/2018");
                driver.FindElementByCssSelector("button[class^=applyBtn").Click();

                System.Threading.Thread.Sleep(2000);

                //Gather all the elements that are are in the results table
                var test = driver.FindElementsByCssSelector("table[id=resultsTable] tbody > tr");

                //ensure 2 data sets are gotten
                Assert.AreEqual(0, test.Count, "Wrong number of data sets returned");
            }

            using (var driver = new FirefoxDriver())
            {
                driver.Manage().Window.Maximize();
                driver.Navigate().GoToUrl(websiteLink);

                System.Threading.Thread.Sleep(2000);

                //Click the google map marker
                driver.FindElementByCssSelector("div[title='thor']").Click();

                System.Threading.Thread.Sleep(2000);

                //Click the View Details
                driver.FindElementByCssSelector("button[onclick^=DisplayStationDataTable]").Click();      //Click the result range

                System.Threading.Thread.Sleep(2000);

                //Click the results
                driver.FindElementById("resultrange").Click();

                System.Threading.Thread.Sleep(2000); ;

                //Select a valid range
                driver.FindElementByCssSelector("li[data-range-key=\"Custom Range\"]").Click();
                driver.FindElementByCssSelector("input[name=daterangepicker_start]").Clear();
                driver.FindElementByCssSelector("input[name=daterangepicker_start]").SendKeys(@"01/04/2018");
                driver.FindElementByCssSelector("input[name=daterangepicker_end]").Clear();
                driver.FindElementByCssSelector("input[name=daterangepicker_end]").SendKeys(@"01/04/2018");
                driver.FindElementByCssSelector("button[class^=applyBtn").Click();

                System.Threading.Thread.Sleep(2000);

                //Gather all the elements that are are in the results table
                var test = driver.FindElementsByCssSelector("table[id=resultsTable] tbody > tr");

                //ensure 2 data sets are gotten
                Assert.AreEqual(0, test.Count, "Wrong number of data sets returned");
            }
        }
    }
}
