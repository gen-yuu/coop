var socket = io(); // WebSocket接続を初期化
// サーバーからユーザのNFCが追加されたときの処理
socket.on('item_added', function(data){
    var itemName = data.itemName;
    var itemPrice = data.itemPrice;
    var stockNum = data.stockNum;
    var itemClass = data.itemClass;
    var Barcode = data.Barcode;
    document.getElementById("barcode").value = Barcode;
    document.getElementById("productName").value = itemName;
    document.getElementById("productPrice").value = itemPrice;
    document.getElementById("stockQuantity").value = stockNum;
    document.getElementById("productCategory").value = itemClass;
});

// サーバーからユーザのNFCが追加されたときの処理
socket.on('item_barcode', function(data){
    var Barcode = data.barcode;
    document.getElementById("barcode").value = Barcode;
});