import QtQuick 2.15
import QtGraphicalEffects 1.15


Item{
    Rectangle{
        id : selected
        anchors.fill : parent
        anchors.leftMargin: -4
        anchors.rightMargin: -4
        anchors.topMargin: -4
        anchors.bottomMargin: -4
        radius : 10
        gradient :  Gradient {
                        GradientStop { position: 0.0; color: "#DA22FF" }
                        GradientStop { position: 1.0; color: "#9733EE" }
                    }
        layer.enabled: true
        layer.effect: DropShadow{ horizontalOffset:2;verticalOffset:4;color:"#831499";radius : 2}
    }
    RectangularGlow {
        id: effect
        anchors.fill: selected
        glowRadius: 15
        spread: 0.2
        color: "#DA22FF"
        cornerRadius: selected.radius + glowRadius
    }

    Behavior on opacity{
        NumberAnimation{easing.type: Easing.InOutSine;duration:400}
    }
}