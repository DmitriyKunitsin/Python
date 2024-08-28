import QtQuick 2.15
import QtQuick.Controls 2.15



ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "HelloApp"
    property string currTime: "00:00:00"
    property QtObject backend

   
    Rectangle {
        anchors.fill: parent
        Image {
            sourceSize.width: parent.width
            sourceSize.height: parent.height
            source: "./images.jpg"
            fillMode: Image.PreserveAspectCrop
        }
        }
        Rectangle {
            anchors.fill: parent
            color: "transparent"
            Text {
                anchors {
                    bottom: parent.bottom
                    bottomMargin: 12
                    left: parent.left
                    leftMargin: 12
                }
                text: currTime
                font.pixelSize: 48
                color: "white"
            }
        }
        Connections {
            target: backend
            function onUpdated(msg) {
                currTime = msg;
        }
    }

    Text {
        anchors.centerIn: parent
        text: "Hello, World"
        font.pixelSize: 24
    }
}