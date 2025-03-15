import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Item{
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.left: parent.left
    //height: 20
    DragHandler {
        onActiveChanged: if (active) window.startSystemMove();
        target: null
    }
    Row{
        id: titleButtons
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: 4
        spacing: 10
        rightPadding: background.radius + 5
        RoundButton{
            radius:10; width:20;height:20;
            background:Rectangle{
                anchors.fill: parent;color:"#009432";radius:10
                layer.enabled: true
                layer.effect: DropShadow{ horizontalOffset:0;verticalOffset:2;color:"#80ca99";}   
            }
            onClicked: window.showMinimized()
        }
        RoundButton{
            property bool min: true
            radius:10; width:20;height:20;
            background:Rectangle{
                anchors.fill: parent;color:"#FFC312";radius:10
                layer.enabled: true
                layer.effect: DropShadow{ horizontalOffset:0;verticalOffset:2;color:"#ffe7a0";}    
            }
            onClicked: {min?window.showMaximized():window.showNormal();min=!min}
        }
        RoundButton{
            radius:10; width:20;height:20;
            background:Rectangle{
                anchors.fill: parent;color:"#EA2027";radius:10 
                layer.enabled: true
                layer.effect: DropShadow{ horizontalOffset:0;verticalOffset:2;color:"#f7a6a9";}    
            }
            onClicked: window.close()
        }
    }
}