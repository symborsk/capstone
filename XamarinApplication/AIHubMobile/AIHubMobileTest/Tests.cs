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
    }
}

