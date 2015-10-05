# KMACTF_Crypto200_PaddingOracleAttack
Bài crypto200 này làm team Gaara mình cực kì tiếc nuối luôn vì lẽ ra chắc chắn sẽ làm được cơ mà kiểu gửi data lên mà không có eception nên hơi khó để team mình tìm ra được cách send data chuẩn
Đây là một bài crypto có dạng PaddingOracleAttack. 
các bạn có thể tìm hiểu thêm về dạng tấn công này ở đây 

<a href="http://www.exploresecurity.com/padding-oracle-decryption-attack/">PaddingOracle</a>

Đối với thử thách này chúng ta cần nắm rõ cơ chế mã hóa và giải mã của chế độ mã khối CBC. Thứ 2 là cần nắm rõ cơ chế checkpadding.

1, Chế độ giải mã CBC như sau:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/135065266@N08/21972095591/in/datetaken/" title="Slide3"><img src="https://farm6.staticflickr.com/5683/21972095591_799075d6bc_z.jpg" width="640" height="480" alt="Slide3"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

Đối với khối cipher đầu tiên, chúng ta sau khi giải mã xong cipher sẽ đem kết quả đó xor với IV. Trong thử thách này mã hóa AES 128bit nên IV bao gồm 128bit.

Đối với những khối mã tiếp theo ta sẽ coi khối mã trước nó như là vector IV như ở khối một, để sau mỗi khi mã hóa xong chúng ta sẽ trước dụng khối mã trước đó để xor.

2, Tiếp theo ta sẽ tìm hiểu về cơ chế checkpadding nhé.
Thử thách cho ta 1 server dùng để checkpadding. Nếu padding đúng sẽ trả về mã lỗi 404, padding sai trả về mã lỗi 4
03.

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/135065266@N08/21962314675/in/datetaken/" title="Slide5"><img src="https://farm1.staticflickr.com/626/21962314675_bcb393d45b_z.jpg" width="640" height="480" alt="Slide5"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

Như trên hình chúng ta thấy các giá trị: C là bản mã, INT là giá trị sau khi dùng khóa giải mã, IV là vector IV, P là bản rõ. Những giá trị mà ta biết là bản mã, và vector IV. Công việc ta cần giải quyết là tìm P dựa vào cơ chế padding.
Vậy việc chúng ta cần phải làm là tìm đuợc INT và lấy INT xor với IV là ra được khối rõ đầu tiên.
Vậy làm như thế nào để ta có thể tìm lại được INT. Và muốn hiểu rõ hơn về padding thì cần phải tìm hiểu PKCS#5 và <a href = "https://en.wikipedia.org/wiki/Padding_%28cryptography%29#PKCS7">PKCS#7</a> nhé.

Đây là các bước để mình kiểm tra padding nhé:
- Bước đầu tiên ta sẽ gửi 1 đoạn 00000000000000000000000000000000a5936cfd61e8d5dc6b6b6d121d2a7124. 16bytes đầu tiên là 1 vector IV giả định, 16bytes sau là khối cipher đầu tiên
- khi đó server sẽ trả về cho chúng ta mã lỗi 403 vì padding sai. Vì sao. vì khi ta gửi đoạn kia lên server, server sẽ tách làm 2 nửa. Server sẽ thực hiện giải mã đoạn mã đầu tiên, như vậy coi như ta có thể biết đựoc giá trị INT (Giá trị này của server giúp chúng ta checkpadding). 
- Chúng ta sẽ tăng bytes cuối cùng(bytes 16) của IV giả định lên cho đến khi server trả về mã lỗi 404 tức là bytes cuối cùng của P sẽ là 0x01
- '0000000000000000000000000000009aa5936cfd61e8d5dc6b6b6d121d2a7124' tăng đến giá trị '9a' ta sẽ thu được mã lỗi 404.
- ta sẽ lấy giá trị '9a' xor với 0x01 ta thu đựoc chính xác bytes cuối cùng của INT. là 0x9b
- <a data-flickr-embed="true"  href="https://www.flickr.com/photos/135065266@N08/21775406369/in/datetaken/" title="Slide6"><img src="https://farm1.staticflickr.com/580/21775406369_80af01f590_z.jpg" width="640" height="480" alt="Slide6"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>
- 
- tiếp theo ta sẽ cần cho 2 bytes cuối cùng của plain thành 0x02 0x02 thì ta sẽ tiếp tục thu được mã 404
- Vậy ta cần tăng bytes cuối của vector IV giả định lên để khi giá trị IV xor với 0x02 vẫn thu đựoc giá trị của INT là 0x9b. Đơn giản là ta sẽ lấy 0x9a ^ 0x01 ^ 0x02 thì chính là giá trị bytes cuối của IV. thu đựoc kết quả đó nhờ định luật thần thánh của phép xor mà chúng ta đã biết :)).
- vậy đoạn mã thứ 2 ta sẽ gửi lên server sẽ là '00000000000000000000000000000099a5936cfd61e8d5dc6b6b6d121d2a7124'. Ta sẽ thu đựoc mã lỗi 403. Lúc này bytes 16 của P đã là 0x02 nên ta cần tăng bytes 15 của IV lên để đến khi nào bytes 15 của P cũng là 0x02 ta sẽ thu đựoc mã 404
- '00000000000000000000000000006d99a5936cfd61e8d5dc6b6b6d121d2a7124' đây sẽ là kết quả của lần thứ 2
- Cứ liên tiếp như vậy 16 vòng lặp ta sẽ thu được 1 vector IV giả định gồm đầy đủ 16 bytes
- Đây là kết quả của 16 vòng lặp '72936c3ac97a16f44f7c095f1a8f7f8ba5936cfd61e8d5dc6b6b6d121d2a7124' 16bytes đầu tiên sẽ là vector giả định '72936c3ac97a16f44f7c095f1a8f7f8b'
- Tiếp theo từ giá trị này ta có thể thu đựoc chính xác giá trị của INT bằng cách đem lần lượt từng bytes xor với 0x10 nhé. Cái này các bạn nhìn hình giải mã của chế độ CBC thì sẽ hiểu vì sao nhé. Tiếp theo đó ta sẽ lấy kết quả vừa thu được xor vơi vector IV thật sự đầu tiên thì sẽ thu đựoc bản rõ của khối đầu tiền.
- Đối với những khối tiếp theo ta sẽ sử dụng bản mã của khổi trước đó làm vector IV.
- <a data-flickr-embed="true"  href="https://www.flickr.com/photos/135065266@N08/21936144926/in/datetaken/" title="Slide7"><img src="https://farm1.staticflickr.com/632/21936144926_204edeb630_z.jpg" width="640" height="480" alt="Slide7"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>
- 
Thực hiện hết 6 vòng lặp cho 6 khối ta sẽ thu được kết quả cẩn tìm là:
<h5>Got it. NEPTUNE is number 1! The flag is KMA_CTF{b4d_1mpl3m3nt4t10n_a3s_cbc_m0d3}</h5>


Mọi người có thể code lại và thử nhé vì server chỉ mở hết ngày 5/10/2015

Thank a Nguyễn Tuấn Anh đã ra một bài khá hay :)

