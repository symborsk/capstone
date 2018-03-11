/**
 * Test.cs
 * By: John Symborski
 * Capstone Group 2
 * The UI tests and initializations of the 
 * */

using System;
using System.IO;
using System.Linq;
using NUnit.Framework;
using Xamarin.UITest;
using Xamarin.UITest.Queries;

namespace AIHubMobileTest
{
    [TestFixture(Platform.Android)]
    [TestFixture(Platform.iOS)]
    public class Tests
    {
        IApp app;
        Platform platform;

        public Tests(Platform platform)
        {
            this.platform = platform;
        }

        [SetUp]
        public void BeforeEachTest()
        {
            if(platform == Platform.Android)
            {
                app = ConfigureApp.Android.Debug().ApkFile(@"C:\Projects\Capstone\XamarinApplication\AIHubMobile\AIHubMobile\AIHubMobile.Android\bin\Release\com.companyname.AIHubMobile.apk").StartApp();
            }
            else
            {
                app = AppInitializer.StartApp(platform);
            }
        }

        [Test]
        public void AppLaunches()
        {
            app.Screenshot("First screen.");
        }

        [Test]
        public void UpdateOptions()
        {
            app.Tap("Options");
            app.WaitForElement("Mock Option", "Options button did not respond!", new TimeSpan(0, 0, 10));

            //Ensure the update screen redirected to the main screen with
            app.Tap("UPDATE");
            app.WaitForElement("About", "Update command failed", new TimeSpan(0, 0, 10));
        }

        [Test]
        public void ViewAbout()
        {
            app.Tap("About");
            app.WaitForElement("View Web Portal", "About did not respond.", new TimeSpan(0, 0, 10));
        }

    }
}

