/**
 * WeatherItemViewModel.cs
 * By: John Symborski
 * Capstone Group 2
 * Defines the interactions between the views and the model of the weather set item. Also subscribes any messaging services
 * the xamarin application may need to run.
 * */

using System;
using System.Collections.ObjectModel;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using Xamarin.Forms;

namespace AIHubMobile
{
    public class WeatherItemsViewModel : BaseViewModel
    {
        //Collection that can be viewed
        public ObservableCollection<WeatherSet> Items { get; set; }
        public Command LoadItemsCommand { get; set; }

        public WeatherItemsViewModel()
        {
            Title = "View Weather";
            Items = new ObservableCollection<WeatherSet>();
            LoadItemsCommand = new Command(async () => await ExecuteLoadItemsCommand());
            AppOptions options = new AppOptions();

            //Create an inline function of what to do when recieving this message
            MessagingCenter.Subscribe<ChangeOptionsPage, AppOptions>(this, "UpdateOptions", async (obj, option) =>
            {
                var _item = option as AppOptions;
                options = _item;
                await WeatherSet.RefreshWeatherSets();
                await WeatherSet.GetAllWeatherSets();
            });
        }

        //Async load of the items
        async Task ExecuteLoadItemsCommand()
        {
            if (IsBusy)
                return;

            IsBusy = true;

            try
            {
                Items.Clear();
                bool succ = await WeatherSet.RefreshWeatherSets();
                IEnumerable<WeatherSet> items = await WeatherSet.GetAllWeatherSets(true);
                foreach (var item in items)
                {
                    Items.Add(item);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex);
            }
            finally
            {
                IsBusy = false;
            }
        }
    }
}
