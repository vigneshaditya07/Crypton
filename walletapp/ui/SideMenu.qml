import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15

Item{
    implicitHeight: parent.height
    implicitWidth: parent.width*0.05
    property int margin: background.radius

    property int index: 0
    Rectangle{
        //the visual sidebar
        anchors.fill: parent
        color: "#5b1f8f"
        radius: 40
    }
    Rectangle{
        //for straight edge
        anchors.left: parent.horizontalCenter
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        color: "#5b1f8f"
        layer.enabled: true
        layer.effect: DropShadow{ horizontalOffset:6;verticalOffset:0;color:"#d9d9d9";radius : 5}
    }
    ColumnLayout{
        id: columnlayout
        property  int padding: 40
        property size itemsize: Qt.size(0.45*width,0.45*width)
        anchors.fill: parent
        anchors.topMargin: margin + padding //margin will align it with the top of side bar
        anchors.bottomMargin: margin + padding
        spacing: 40
        
        Item{
            property int myindex: 0
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            implicitWidth: 0.45 *parent.width
            implicitHeight: 0.45*parent.width

        MenuSelected{
            anchors.fill:item1;opacity:index==parent.myindex?1:0
        }

        MouseArea{anchors.fill:parent;onClicked:index=parent.myindex}

        Image{
            id: item1
            source: "res/images/home.svg"
            sourceSize: columnlayout.itemsize
        }
        ColorOverlay {
            anchors.fill: item1
            source: item1
            color: index==parent.myindex?"#f6edf7":"#f2b2ff"
        }
        
        }
        Item{
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            implicitWidth: 0.45 *parent.width
            implicitHeight: 0.45*parent.width
            property int myindex: 1

        MenuSelected{
            anchors.fill:item2;opacity:index==parent.myindex?1:0
        }

        MouseArea{anchors.fill:parent;onClicked:index=parent.myindex}

        Image{
            id: item2
            source: "res/images/pay.svg"
            sourceSize: columnlayout.itemsize
        }
        ColorOverlay {
            anchors.fill: item2
            source: item2
            color: index==parent.myindex?"#f6edf7":"#f2b2ff"
        }
        }
        

        //Item{ Layout.fillHeight : true}
        Item{
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            implicitWidth: 0.45 *parent.width
            implicitHeight: 0.45*parent.width
            property int myindex: 2

        MenuSelected{
            anchors.fill:item3;opacity:index==parent.myindex?1:0
        }

        MouseArea{anchors.fill:parent;onClicked:index=parent.myindex}

        Image{
            id: item3
            source: "res/images/history.svg"
            sourceSize: columnlayout.itemsize
        }
        ColorOverlay {
            anchors.fill: item3
            source: item3
            color: index==parent.myindex?"#f6edf7":"#f2b2ff"
        }
        }
        Item{
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            implicitWidth: 0.45 *parent.width
            implicitHeight: 0.45*parent.width
            property int myindex: 3

        MenuSelected{
            anchors.fill:item4;opacity:index==parent.myindex?1:0
        }

        MouseArea{anchors.fill:parent;onClicked:index=parent.myindex}

        Image{
            id: item4
            source: "res/images/explore.svg"
            sourceSize: columnlayout.itemsize
        }
        ColorOverlay {
            anchors.fill: item4
            source: item4
            color: index==parent.myindex?"#f6edf7":"#f2b2ff"
        }
        }
        Item{
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            implicitWidth: 0.45 *parent.width
            implicitHeight: 0.45*parent.width
            property int myindex: 4

        MenuSelected{
            anchors.fill:item5;opacity:index==parent.myindex?1:0
        }

        MouseArea{anchors.fill:parent;onClicked:index=parent.myindex}

        Image{
            id: item5
            source: "res/images/settings.svg"
            sourceSize: columnlayout.itemsize
        }
        ColorOverlay {
            anchors.fill: item5
            source: item5
            color: index==parent.myindex?"#f6edf7":"#f2b2ff"
        }
        }
    }
    
}