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
        public ObservableCollection<WeatherSet> Items { get; set; }
        public Command LoadItemsCommand { get; set; }

        public WeatherItemsViewModel()
        {
            Title = "View Weather";
            Items = new ObservableCollection<WeatherSet>();
            LoadItemsCommand = new Command(async () => await ExecuteLoadItemsCommand());
            AppOptions options = new AppOptions();

            MessagingCenter.Subscribe<ChangeOptionsPage, AppOptions>(this, "UpdateOptions", async (obj, option) =>
            {
                var _item = option as AppOptions;
                options = _item;
                await WeatherSet.RefreshWeatherSets();
                await WeatherSet.GetAllWeatherSets();
            });
        }

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
