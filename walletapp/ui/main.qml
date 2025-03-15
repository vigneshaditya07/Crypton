import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    id: window
    visible: true
    title: "Hello"
    width: 0.75*1920
    height: 0.75*1080
    flags: Qt.FramelessWindowHint | Qt.Window
    //flags: Qt.Window | Qt.CustomizeWindowHint
    color: "transparent"

    Rectangle{
        //the bg rounded rectangle
        id: background
        anchors.fill:parent
        radius: 40
    }

    TitleBar{
        id: titleBar
        height: background.radius
    }

    SideMenu{
        id: sideMenu
    }

    Rectangle{
        id: mainArea
        anchors.left: sideMenu.right
        anchors.top: titleBar.bottom
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.rightMargin: background.radius
        anchors.bottomMargin: background.radius
        anchors.leftMargin: 20

        Item{
            id:stacklayout 
            anchors.fill:parent
            property int currentIndex:sideMenu.index

            Home{
                visible:opacity!=0
                id:home
                property bool active: parent.currentIndex==0
                state: "active"
                onActiveChanged : state=active?"active":"inactive";
                states: [
                    State{
                        name: "active"
                        PropertyChanges{target:home;opacity:1}
                    },
                    State{
                        name: "inactive"
                        PropertyChanges{target:home;opacity:0}
                    }
                ]

                transitions:[
                    Transition{
                        from:"active";to:"inactive";NumberAnimation{target:home;property:"opacity";duration:200}
                    },
                    Transition{
                        from:"inactive";to:"active";NumberAnimation{target:home;property:"opacity";duration:400}
                    }
                ]
                
            }

            Rectangle{
                id:rect
                color:"#dfe6e9"
                radius:30
                anchors.fill:parent
                visible:opacity!=0
                property bool active: parent.currentIndex==1
                state: "inactive"
                onActiveChanged : state=active?"active":"inactive";
                states: [
                    State{
                        name: "active"
                        PropertyChanges{target:rect;opacity:1}
                    },
                    State{
                        name: "inactive"
                        PropertyChanges{target:rect;opacity:0}
                    }
                ]

                transitions:[
                    Transition{
                        from:"active";to:"inactive";NumberAnimation{target:rect;property:"opacity";duration:200}
                    },
                    Transition{
                        from:"inactive";to:"active";NumberAnimation{target:rect;property:"opacity";duration:400}
                    }
                ]
                
            }

        }
    }
}