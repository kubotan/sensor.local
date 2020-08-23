# ライセンスや注意事項
ライブラリや制作物のライセンスは作者に帰属します。なので作者が指定するライセンスが適用されます。
使用したライブラリによる制約を受けない限り、私が作った部分はMITライセンスを適用します。
なお、温度データなどを一般公開するには気象庁の認証を通った機器や登録が必要だったかと思います。その点もご注意ください。

# ラズパイでCRONTABの登録
- arduino unoが出力するCSV形式の値をJSONに変換するバッチを登録します。CRONTABは以下を参考にしてください。
```
@reboot /var/www/html/data/latest.py
@reboot /var/www/html/data/loopWriteMinute.py
@reboot /var/www/html/data/loopWriteHour.py

*/20 * * * * /var/www/html/data/write.py /var/www/html/data/day.json
0 */2 * * * /var/www/html/data/write.py /var/www/html/data/week.json
0 */8 * * * /var/www/html/data/write.py /var/www/html/data/month.json
0 12 */4 * * /var/www/html/data/write.py /var/www/html/data/year.json
```
※公開フォルダにバッチを配置することはセキュリティー上、危険です。これはあくまでもサンプルです。
