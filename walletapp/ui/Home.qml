import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import QtQuick.Layouts 1.15

Item{
    anchors.fill:parent
    property int margin: 10
    FontLoader { id: thin; source: "res/Roboto/Roboto-Light.ttf" }
    FontLoader { id: bold; source: "res/Baloo_Tammudu_2/BalooTammudu2-Medium.ttf" }

    Rectangle{ anchors.fill: parent;color:"#f5f6fa";radius:20;
    anchors.topMargin:-5;anchors.leftMargin:-5;anchors.rightMargin:-5;anchors.bottomMargin:-5
    }

    Rectangle{
        //balance
        id: balance
        anchors.top: parent.top
        anchors.left: parent.left
        height: parent.height/2
        width: parent.width*0.25
        gradient : Gradient {
            GradientStop { position: 0.0; color: "#DA22FF" }
            GradientStop { position: 1.0; color: "#9733EE" }
        }
        radius: 20
        border.color: "#DA22FF"
        border.width: 2
        layer.enabled: true
        layer.effect: DropShadow{ horizontalOffset:6;verticalOffset:6;/*color:"#d9d9d9"*/color:"#b670f3";radius : 8}
        
        Text {
            id: balancetxt
            text: "Balance"
            font.pointSize: 15
            color : "#ead6fc"
            font.family: thin.name
            anchors.bottom: balanceamt.top
            anchors.horizontalCenter : parent.horizontalCenter
        }

        Text {
            id: balanceamt
            //text: "2,000.00 BTC"
            text: Wallet.balance + ' BTC'
            anchors.verticalCenter : parent.verticalCenter
            anchors.horizontalCenter : parent.horizontalCenter
            anchors.horizontalCenterOffset : fontInfo.pixelSize/2.75
            //anchors.left: logo.right
            //anchors.leftMargin: balanceamt.fontInfo.pixelSize/10
            font.pixelSize: parent.width/7.5
            font.family: bold.name
            color : "#ead6fc"
        
        }

        Image{
            id: logo
            source: "res/images/bitcoin-logo.svg"
            anchors.verticalCenter: balanceamt.baseline
            anchors.verticalCenterOffset:-(balanceamt.fontInfo.pixelSize/2.75)
            //anchors.left: parent.left
            //anchors.leftMargin: balanceamt.fontInfo.pixelSize/10
            anchors.right: balanceamt.left
            anchors.rightMargin: balanceamt.fontInfo.pixelSize/10
            sourceSize: Qt.size(balanceamt.fontInfo.pixelSize,balanceamt.fontInfo.pixelSize)
            layer.enabled: true
            layer.effect: DropShadow{ horizontalOffset:0;verticalOffset:2;color:"#f1c40f";radius : 4}
        }
        Rectangle{
            anchors.left: received.left
            anchors.right: receivedlbl.right
            anchors.top: received.top
            anchors.bottom: received.bottom
            anchors.leftMargin : -4
            anchors.rightMargin: -4
            color: "#C9FFE2"
            radius: 5
        }

        Rectangle{
            id: received
            anchors.top: balanceamt.bottom
            anchors.left: parent.left
            anchors.leftMargin: parent.width*0.2
            height:parent.width*0.075; width:parent.width*0.075
            color :"#66ff92"
            radius : 10
            Image{
                source:"res/images/south_west_black_24dp.svg"
                sourceSize: Qt.size(parent.width,parent.width)
            }
        }

        
        Label{
            id: receivedlbl
            anchors.left: received.right
            anchors.leftMargin: 5
            anchors.verticalCenter: received.verticalCenter
            text : "+2500"
            font.family: thin.name
            font.pixelSize: parent.width*0.075
            color: "#4B7F52"
        }
        Rectangle{
            anchors.left: sent.left
            anchors.right: sentlbl.right
            anchors.top: sent.top
            anchors.bottom: sent.bottom
            anchors.leftMargin : -4
            anchors.rightMargin: -4
            color: "#ffcccc"
            radius: 5
        }
            
        Rectangle{
            id: sent
            anchors.left: receivedlbl.right
            anchors.leftMargin: parent.width*0.2
            anchors.top : received.top
            height:parent.width*0.075; width: parent.width*0.075
            color :"#ff8080"
            radius :10
            Image{
                source:"res/images/north_east_black_24dp.svg"
                sourceSize: Qt.size(parent.width,parent.width)
            }
        }
        Label{
            id: sentlbl
            anchors.left: sent.right
            anchors.leftMargin: 5
            anchors.verticalCenter: sent.verticalCenter
            text : "-500"
            font.family: thin.name
            font.pixelSize: parent.width*0.075
            color: "#ff3333"
        }
            
    }
    
    Rectangle{
        //quickpay
        id: quickPay
        anchors.top: balance.top
        anchors.left: balance.right
        anchors.bottom: balance.bottom
        anchors.right: contacts.left
        anchors.leftMargin:60
        radius: 20
        border.color: "#d9d9d9"
        border.width: 2
        color:"#ffffff"
        layer.enabled: true
        layer.effect: DropShadow{ horizontalOffset:6;verticalOffset:6;color:"#d9d9d9";radius : 8}

        MouseArea{anchors.fill:parent;onClicked:forceActiveFocus()}

        Label { //quipay label
            id:quickpaytxt
            text: "Quick Pay"
            font.pointSize: 15
            topPadding: 20
            leftPadding: 20
            font.family: thin.name
        }

        Label{ //adrress label
            id:addresslabel
            text: "Address"
            anchors.bottom: addressfield.top
            anchors.left: addressfield.left
            anchors.leftMargin: 10
            font.family : thin.name
            font.pixelSize: 15
        }
        TextField{ //addressfield
            id: addressfield
            property string dscolor: "#d9d9d9"
            property string bdcolor : "grey"
            anchors.left:parent.left
            anchors.leftMargin: 20
            anchors.top: quickpaytxt.bottom
            anchors.topMargin: 40
            anchors.right: parent.right
            anchors.rightMargin: parent.width*0.20
            implicitHeight:parent.height*0.1
            background: Rectangle{radius: 10;border.color:addressfield.bdcolor;
            Behavior on border.color{
                ColorAnimation{duration:200;easing.type: Easing.OutSine}
            }
            }
            layer.enabled: true
            layer.effect: DropShadow{horizontalOffset:4;verticalOffset:4;color:addressfield.dscolor;radius :6
            Behavior on color{
                ColorAnimation{duration:200;easing.type: Easing.OutSine}
            }
            }
            font.family : thin.name
            font.pixelSize: implicitHeight/2
            validator: RegularExpressionValidator { regularExpression: /[0-9a-zA-Z]+/ }
            states :[
                State{
                    name : "unselected"
                    when : !addressfield.activeFocus
                    PropertyChanges{ target: addressfield; bdcolor:"grey" }
                    PropertyChanges{ target: addressfield; dscolor:"#d9d9d9" }
                },
                State{
                    name : "selected"
                    when : addressfield.activeFocus
                    PropertyChanges{ target: addressfield; bdcolor:"#0984e3" }
                    PropertyChanges{ target: addressfield; dscolor:"#74b9ff" }
                },
                State{
                    name : "invalid"
                    PropertyChanges{ target: addressfield; bdcolor:"#ee5253" }
                    PropertyChanges{ target: addressfield; dscolor:"#ff6b6b" }
                }

            ]
        }

        Label{ // amount label
            id:amountlabel
            text: "Amount"
            anchors.bottom: amountfield.top
            anchors.left: amountfield.left
            anchors.leftMargin: 10
            //anchors.topMargin: 40
            font.family : thin.name
            font.pixelSize: 15
        }

        TextField{ //amountfield
            id:amountfield
            property string dscolor: "#d9d9d9"
            property string bdcolor : "grey"
            anchors.left:parent.left
            anchors.leftMargin: 20
            anchors.top: addressfield.bottom
            anchors.topMargin: 40
            anchors.right: paybutton.left
            anchors.rightMargin: 40
            implicitHeight:parent.height*0.1
            background: Rectangle{border.color:amountfield.bdcolor;radius: 10;
            Behavior on border.color{
                ColorAnimation{duration:200;easing.type: Easing.OutSine}
            }
            }
            layer.enabled: true
            layer.effect: DropShadow{ horizontalOffset:4;verticalOffset:4;color:amountfield.dscolor;radius :6
            Behavior on color{
                ColorAnimation{duration:200;easing.type: Easing.OutSine}
            }
            }
            font.family : thin.name
            font.pixelSize: implicitHeight/2
            validator: RegularExpressionValidator { regularExpression: /[0-9]+\.[0-9]{1,4}/ }
            states :[
                State{
                    name : "unselected"
                    when : !amountfield.activeFocus
                    PropertyChanges{ target: amountfield; bdcolor:"grey" }
                    PropertyChanges{ target: amountfield; dscolor:"#d9d9d9" }
                },
                State{
                    name : "selected"
                    when : amountfield.activeFocus
                    PropertyChanges{ target: amountfield; bdcolor:"#0984e3" }
                    PropertyChanges{ target: amountfield; dscolor:"#74b9ff" }
                },
                State{
                    name : "invalid"
                    PropertyChanges{ target: amountfield; bdcolor:"#ee5253" }
                    PropertyChanges{ target: amountfield; dscolor:"#ff6b6b" }
                    PropertyChanges{ target: amountfield; color:"#ff6b6b" }
                }

            ]
        }

        Button{
            id : paybutton
            text: "Pay"
            onClicked : {
                var payvalid=Wallet.checkPay(addressfield.text,amountfield.text);
                if(!payvalid[0]) {addressfield.state = "invalid";}
                if(!payvalid[1]) {amountfield.state = "invalid";}
            }
            contentItem: Text {
                text: paybutton.text
                font.pixelSize: quickPay.width/25
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            anchors.verticalCenter:amountfield.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: parent.width*0.25
            layer.enabled: true
            layer.effect: DropShadow{ horizontalOffset:2;verticalOffset:4;color:paybutton.hovered?"#27a758":"#9918b3";radius:6
            Behavior on color{
                ColorAnimation{duration:100;easing.type: Easing.OutSine}
            }
            }
            background : Rectangle{
                            radius:40
                            implicitWidth: quickPay.width*0.20
                            color: paybutton.down?"#32d771":(paybutton.hovered?"#38ef7d":"#DA22FF")
                            Behavior on color{
                                ColorAnimation{duration:100;easing.type: Easing.OutSine}
                            }
                                            
                        }
        }

        Label{ 
            id:quickreceivetxt
            text: "Quick Receive"
            anchors.left:parent.left
            anchors.leftMargin: 20
            anchors.top: amountfield.bottom
            anchors.topMargin: 20
            font.family: thin.name
            font.pointSize: 15
        }
        Label{ //receive adrress label
            id:rec_addresslabel
            text: "Your address"
            anchors.bottom: rec_addressfield.top
            anchors.left: rec_addressfield.left
            anchors.leftMargin: 10
            font.family : thin.name
            font.pixelSize: 15
        }
        TextField{ //addressfield
            id: rec_addressfield
            anchors.left:parent.left
            anchors.leftMargin: 20
            anchors.top: quickreceivetxt.bottom
            anchors.topMargin: parent.height*0.1
            anchors.right: parent.right
            anchors.rightMargin: parent.width*0.20
            text: "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"
            readOnly: true
            implicitHeight:parent.height*0.1
            background: Rectangle{
                border.color: "grey";radius: 10
            }
            font.family : thin.name
            font.pixelSize: implicitHeight/2
            Button{
                    id:copybutton
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.topMargin: 4
                    anchors.rightMargin: 4
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 4
                    width:copybutton.height
                    background: Rectangle{color: copybutton.down ? "#dcaae6" : "#f4bdff";radius:10}
                    icon.source : "res/images/copy.svg"
                    icon.color: "#5c3165"
                    TextField{id:cpyfield;text:rec_addressfield.text;visible:false}
                    onClicked: { cpyfield.selectAll();cpyfield.copy()}
                }
        }
    }
    Rectangle{
        id : contacts
        anchors.top : balance.top
        anchors.bottom: balance.bottom
        anchors.right: parent.right
        radius: 15
        width: parent.width*0.25
        border.color: "#d9d9d9"
        border.width: 2
        layer.enabled: true
        layer.effect: DropShadow{ horizontalOffset:6;verticalOffset:6;color:"#d9d9d9";radius : 8}


        Rectangle{
            id: header
            anchors.top: contacts.top
            anchors.left: contacts.left
            anchors.right: contacts.right
            anchors.leftMargin: 2;anchors.topMargin: 2;anchors.rightMargin: 2
            height: parent.height*0.15
            radius: 15
            //color: "#DA22FF"
            color:"#aa00ff"
            layer.enabled: true
            layer.effect: DropShadow{ horizontalOffset:0;verticalOffset:4;color:"#7700b3";radius:4}


            Button{
                id: addcontact
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.topMargin: 8
                anchors.rightMargin: 8
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 8
                width: addcontact.height
                background: Rectangle{color: addcontact.hovered?"#00fa92":"#00e183";radius:addcontact.height*0.40}
                icon.source : "res/images/addcontact.svg"
                icon.color: "#00321d"
                onClicked: contactpopup.open() 
            }
        }



        Label{
            anchors.fill: header
            text: "Contacts"
            //color: "#ead6fc"
            color: "white"
            leftPadding: 20
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: header.height*0.5
            font.family: thin.name
        }
        

        ListModel{
            id: contactmodel
            ListElement{name:"Elan Thamil";address:"a12b57cdf5dc1275"}
            ListElement{name:"Ganapathi";address:"ff224ad56c654"}
            ListElement{name:"Pawan Kumar";address:"1277a5b54c55e454"}
            ListElement{name:"Sanjay Sundar";address:"ecc7248a65b5de54f"}
            ListElement{name:"Vignesh Aditya";address:"2a5b749cd56e5f"}
            ListElement{name:"Vivekanand";address:"c52a2e25bc6d8ee8f"}
            ListElement{name:"testcontact";address:"testaddress"}
        }

        Component{
            id: contactdelegate
            Rectangle{
                height: ListView.view.height*0.15
                radius: 10
                //border.color: "grey"
                width: ListView.view.width
                Label{
                    id : conlabel
                    text : name[0].toUpperCase()
                    font.pixelSize: height*0.75
                    font.family: thin.name
                    horizontalAlignment:Text.AlignHCenter
                    verticalAlignment:Text.AlignVCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.top: parent.top
                    anchors.topMargin : 4
                    height: parent.height*0.85
                    width: height
                    color: "white"
                    background : Rectangle{
                        id : conicon
                        anchors.left: parent.left
                        anchors.verticalCenter : parent.verticalCenter
                        height: parent.height
                        width: height
                        radius: height*0.5
                        color: iconcolor
                    }
                }
                Label{
                    text: name
                    anchors.left: conlabel.right
                    anchors.leftMargin: 8
                    width: parent.width
                    height: parent.height
                    //leftPadding: 20
                    //horizontalAlignment:Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.pixelSize: parent.width*0.075
                    font.family: thin.name
                }
                TextEdit{id:copytxtedit;visible:false;text:address;readOnly:true}
                layer.enabled: true
                layer.effect: DropShadow{ horizontalOffset:0;verticalOffset:4;color:"#cccccc";radius:2}
                Button{
                    id:copybutton
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.topMargin: 4
                    anchors.rightMargin: 4
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 4
                    width:copybutton.height
                    //background: Rectangle{color: copybutton.down ? "#dcaae6" : "#f4bdff";radius:10}
                    background: Rectangle{color: copybutton.down ? "#d580ff" : "#eeccff";radius:10}
                    icon.source : "res/images/copy.svg"
                    icon.color: "#5c3165"
                    onClicked: { copytxtedit.selectAll();copytxtedit.copy()}
                }
            }
        }

        ListView{
            anchors.top:header.bottom;anchors.bottom: parent.bottom;anchors.left: parent.left;anchors.right: parent.right
            anchors.leftMargin: 16;anchors.topMargin: 16;anchors.rightMargin: 16;anchors.bottomMargin: 16
            //model: contactmodel
            model: Wallet.contactModel
            delegate: contactdelegate
            spacing: 4
            clip : true
        }
        
    }
    Rectangle{
        //recent transactions
        id: recentTx
        anchors.top: balance.bottom
        anchors.bottom: parent.bottom
        anchors.left: balance.left
        anchors.right: parent.right
        anchors.topMargin: margin;
        radius: 20
        border.color: "#d9d9d9"
        color : "#fbfbfd"
        border.width: 2
        layer.enabled: true
        layer.effect: DropShadow{ horizontalOffset:6;verticalOffset:6;color:"#d9d9d9";radius : 8}
        Image{
            anchors.right : parent.right
            anchors.bottom : parent.bottom
            anchors.rightMargin : 16
            anchors.bottomMargin : 8
            source: "res/bitcoinbg.jpg"
            height : parent.height*0.95
            width :  parent.height*0.95
            opacity : 0.15
        }
        Text {
            id: recenttxt
            text: "Recent Transactions"
            font.pointSize: 12
            topPadding: 20
            leftPadding: 20
            color: "#474747"
            font.family: thin.name
        
        }

        Rectangle{
            anchors.top: recenttxt.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 20
            anchors.leftMargin: 5
            anchors.rightMargin: 5
            color: "transparent"

            ListModel{
                id:recentTxmodel
                ListElement{name:"testaddress";amount:-10;message:"Paid for coffee☕"}
                ListElement{name:"test123";amount:40;message:" - "}
            }

            Component{
                id:recentTxdelegate
                Rectangle{
                    implicitWidth:ListView.view.width
                    implicitHeight: 40
                    //color: "yellow"
                    radius: 10
                    border.color: "#d9d9d9"
                    layer.enabled: true
                    layer.effect: DropShadow{ horizontalOffset:0;verticalOffset:2;color:"#d9d9d9";radius : 4}
                
                Label{
                    id: r_name
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    height: parent.height
                    width: parent.width*0.3
                    text: name
                    font.pixelSize:height*0.45
                    font.family: thin.name
                    verticalAlignment:Text.AlignVCenter
                    elide: Text.ElideMiddle
                }
                ToolSeparator{id:namesep;anchors.left:r_name.right}
                Label{
                    id:r_amount
                    anchors.left:namesep.right
                    height: parent.height
                    width: parent.width*0.075
                    text: amount>0?"+"+amount:amount
                    color: amount>=0?"#4B7F52":"#ff3333"
                    font.pixelSize:height*0.5
                    font.family: thin.name
                    verticalAlignment:Text.AlignVCenter
                    horizontalAlignment:Text.AlignHCenter
                    
                }
                ToolSeparator{id:amountsep;anchors.left:r_amount.right}
                Label{
                    id:r_message
                    anchors.left:amountsep.right
                    anchors.leftMargin: 10
                    anchors.right:parent.right
                    height: parent.height
                    text: message
                    font.pixelSize:height*0.5
                    font.family: thin.name
                    verticalAlignment:Text.AlignVCenter
                }
                }
            }

            ListView{
                anchors.fill: parent
                anchors.topMargin: 10
                anchors.leftMargin: 10
                model: recentTxmodel
                delegate: recentTxdelegate
                spacing: 8
                clip : true
            }
        }
    }

    Popup{
        id : contactpopup
        anchors.centerIn: Overlay.overlay
        width: 700
        height: 400
        focus: true
        modal : true
        Overlay.modal : Rectangle{ color:"#992d3436";radius : 40}
        property point globalc: Qt.point(0,0)
        background : Rectangle{
            id : popuprect
            anchors.fill: parent
            radius : 20
            //color : "transparent"
            //opacity : 0.8
            border.color : "grey"
        
            FastBlur{
                id : fblur
                anchors.fill: parent
                radius : 40
                source: ShaderEffectSource {
                    sourceItem: home
                    sourceRect: Qt.rect(contactpopup.globalc.x-(sideMenu.width+20),contactpopup.globalc.y-titleBar.height,contactpopup.width,contactpopup.height)
                    // 20 is the left margin of mainarea and rect is in global co ordinates
                }
                opacity : 0.5
                layer.enabled: true
                layer.effect: OpacityMask {
                    maskSource:
                        Rectangle {
                            anchors.centerIn: parent
                            width: fblur.width
                            height: fblur.height
                            radius: 20
                        }
                    }
            }
        }
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        onOpened : globalc = mapToItem(home,x,y);

        Label{
            id: addclbl
            text: "Add Contact"
            leftPadding : 20
            font.pixelSize: contactpopup.width*0.07
            font.family: thin.name
            color : "#353b48"

        }

        TextField{ 
            id: cname
            //anchors.left:parent.left
            //anchors.leftMargin: 20
            anchors.horizontalCenter : parent.horizontalCenter
            anchors.top: addclbl.bottom
            anchors.topMargin: 40
            implicitHeight:parent.height*0.125
            implicitWidth: parent.width*0.75
            background: Rectangle{border.color:cname.activeFocus?"#0984e3":"grey";radius: 10;
            Behavior on border.color{
                ColorAnimation{duration:200;easing.type: Easing.OutSine}
            }
            }
            layer.enabled: true
            layer.effect: DropShadow{ horizontalOffset:4;verticalOffset:4;color:cname.activeFocus?"#74b9ff":"#d9d9d9";radius :8
            Behavior on color{
                ColorAnimation{duration:200;easing.type: Easing.OutSine}
            }
            }
            font.family : thin.name
            font.pixelSize: implicitHeight/2
            placeholderText : "Name"
            validator: RegularExpressionValidator { regularExpression: /[0-9A-Za-z ]{1,20}/ }
        }

        TextField{ 
            id: caddr
            //anchors.left:parent.left
            //anchors.leftMargin: 20
            anchors.horizontalCenter : parent.horizontalCenter
            anchors.top: cname.bottom
            anchors.topMargin: 40
            implicitHeight:parent.height*0.125
            implicitWidth: parent.width*0.75
            background: Rectangle{border.color:caddr.activeFocus?"#0984e3":"grey";radius: 10;
            Behavior on border.color{
                ColorAnimation{duration:200;easing.type: Easing.OutSine}
            }
            }
            layer.enabled: true
            layer.effect: DropShadow{ horizontalOffset:4;verticalOffset:4;color:caddr.activeFocus?"#74b9ff":"#d9d9d9";radius :8
            Behavior on color{
                ColorAnimation{duration:200;easing.type: Easing.OutSine}
            }
            }
            font.family : thin.name
            font.pixelSize: implicitHeight/2
            placeholderText : "Address"
            validator: RegularExpressionValidator { regularExpression: /[0-9A-Za-z]{8,40}/ }
        }

        Button{
            id : caddbtn
            text: "Add"
            onClicked : {Wallet.addContact(cname.text,caddr.text);contactpopup.close();cname.clear();caddr.clear()}
            implicitHeight: contactpopup.width*0.070
            contentItem: Text {
                text: caddbtn.text
                font.pixelSize: caddbtn.height/2
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            anchors.top : caddr.bottom
            anchors.topMargin : 45
            //anchors.left: parent.left
            anchors.left : cname.left
            anchors.leftMargin: 40
            layer.enabled: true
            layer.effect: DropShadow{ horizontalOffset:2;verticalOffset:4;color:"#27a758";radius:6}
            background : Rectangle{
                            radius:40
                            implicitWidth: contactpopup.width*0.20
                            color: caddbtn.down?"#32d771":"#38ef7d"
                            Behavior on color{
                                ColorAnimation{duration:100;easing.type: Easing.OutSine}
                                }
                            }
            }


        Button{
            id : ccancelbtn
            text: "Cancel"
            onClicked : {contactpopup.close();cname.clear();caddr.clear()}
            implicitHeight: contactpopup.width*0.070
            contentItem: Text {
                text: ccancelbtn.text
                font.pixelSize: ccancelbtn.height/2
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            anchors.top : caddr.bottom
            anchors.topMargin : 45
            anchors.left: caddbtn.right
            anchors.leftMargin: 120
            layer.enabled: true
            layer.effect: DropShadow{ horizontalOffset:2;verticalOffset:4;color:"#a4161b";radius:6}
            background : Rectangle{
                            radius:40
                            implicitWidth: contactpopup.width*0.20
                            color: ccancelbtn.down?"#ee5253":"#ff6b6b"
                            Behavior on color{
                                ColorAnimation{duration:100;easing.type: Easing.OutSine}
                                }
                            }
            }

    }
}