Vue.use(window["vue-js-modal"].default); //evite d'installer webpack juste pour import VModal from 'vue-js-modal'
new Vue({
    delimiters: ['${', '}'],
    el: '#app',
    data: {
        baseUrlAPI: '/api/orders/?format=json',
        orders: [],
        currentOrder: {
            idFlux:null,
            marketplace:null,
            order_amount:null,
            order_currency:null,
            order_id:null,
            order_mrid:null,
            order_purchase_date:null,
            order_purchase_heure:null,
            order_refid:null,
        },
        search_order_id:null,
        search_marketplace:null,
        search_order_purchase_date_min:null,
        search_order_purchase_date_max:null,
        loading:true,
    },
    watch: {
        search_order_id : function(){ this.refresh(); },
        search_marketplace : function(){ this.refresh(); },
        search_order_purchase_date_min : function(){ this.refresh(); },
        search_order_purchase_date_max : function(){ this.refresh(); },
    },
    mounted() {
        this.loadOrders();
    },
    methods: {
        refresh: function() {
            let urlApi = this.baseUrlAPI;
            if (this.search_order_id) {
                urlApi += '&order_id__icontains=' + this.search_order_id.trim();
            }
            if (this.search_marketplace) {
                urlApi += '&marketplace__icontains=' + this.search_marketplace.trim();
            }
            let dateMin = this.search_order_purchase_date_min ? this.search_order_purchase_date_min.trim() : '';
            let dateMax = this.search_order_purchase_date_max ? this.search_order_purchase_date_max.trim() : '';
            if(dateMin.length===0) dateMin = '0001-01-01';
            if(dateMax.length===0) dateMax = '9999-01-01';
            urlApi += '&order_purchase_date__range=' + dateMin + ',' + dateMax;
            this.loadOrders(urlApi);
        },
        loadOrders: function(urlApi){
            if(!urlApi){
                urlApi = this.baseUrlAPI;
            }
            this.loading = true;
            let self = this;
            axios.get(urlApi).then(function (response) {
                self.orders = response.data;
                self.loading=false;
            });
        },
        showOrder: function(index) {
            this.currentOrder = this.orders[index];
            this.$modal.show('order');
        },
    }
});
