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
            Title = "Browse";
            Items = new ObservableCollection<WeatherSet>();
            LoadItemsCommand = new Command(async () => await ExecuteLoadItemsCommand());

            //MessagingCenter.Subscribe<NewItemPage, Item>(this, "AddItem", async (obj, item) =>
            //{
            //    var _item = item as Item;
            //    Items.Add(_item);
            //    await DataStore.AddItemAsync(_item);
            //});
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
