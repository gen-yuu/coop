var socket = io(); // WebSocket接続を初期化
var nfc_id = ''; // userのNFC_ID


// サーバーからユーザのNFCが追加されたときの処理
socket.on('user_nfc', function(data){
    nfc_id = data.nfc_id;
    document.getElementById("nfcId").value = nfc_id;
});

// DBにuser情報があったとき、その内容を反映させる
socket.on('user_info', function(data){
    var user_id = data.user_id;
    var userName = data.userName;
    var nfc_id = data.nfc_id;
    var grade = data.grade;
    var balance = data.balance;
    document.getElementById("nfcId").value = nfc_id;
    document.getElementById("userName").value = userName;
    document.getElementById("userYear").value = grade;
    document.getElementById("balance").value = balance;
});

// チャージ額が1以上の時にPWの入力を求める
document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('form');

    form.onsubmit = function(event) {
        var chargeAmount = document.getElementById('charge').value;

        // チャージ額が1以上の場合、パスワードの入力を求める
        if (chargeAmount >= 1) {
            event.preventDefault(); // フォームの送信を一時停止
            var password = prompt("チャージを行うにはパスワードを入力してください:");

            // パスワードが正しい場合のみフォームを送信
            if (password === "703") {
                form.submit(); // フォームの送信を続行
            } else {
                alert("エラー: パスワードが正しくありません。");
            }
        } else {
             // チャージ額が1未満の場合は、直接送信
             form.submit();
        }
    };
});
