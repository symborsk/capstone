﻿
using Foundation;
using UIKit;

namespace AIHubMobile.iOS
{
	[Register("AppDelegate")]
	public partial class AppDelegate : global::Xamarin.Forms.Platform.iOS.FormsApplicationDelegate
	{
		public override bool FinishedLaunching(UIApplication app, NSDictionary options)
		{
			global::Xamarin.Forms.Forms.Init();
			LoadApplication(new App());

            //If in the test cloud enable the service
            #if ENABLE_TEST_CLOUD
                        Xamarin.Calabash.Start();
            #endif

            return base.FinishedLaunching(app, options);

       
        }
    }
}
