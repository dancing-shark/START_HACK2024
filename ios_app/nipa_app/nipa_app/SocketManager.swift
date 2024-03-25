//
//  SocketManager.swift
//  nipa_app
//
//  Created by Pascal Weißleder on 24.03.24.
//

import SocketIO
import Foundation
import AVFoundation

class SocketIOManager: NSObject, AVAudioPlayerDelegate, ObservableObject {
    var manager: SocketManager!
    var socket: SocketIOClient!
    
    private let audioEngine = AVAudioEngine()
    var audioPlayer: AVAudioPlayer?
    
    @Published var isPlaying = false
    @Published var isRequesting = false
    
 
    
    private var outputFile: AVAudioFile?

    private let outputAudioFileName: String = "recording.m4a"
    private let recievedAudioFileName:  String = "received_audio.wav"
    
    private let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    
    private let urlPath: URL = URL(string: "http://192.168.2.155:8000")!

    override init() {
        super.init()
        
        // Setup socket connection
        manager = SocketManager(socketURL: urlPath, config: [.log(true), .compress])
        socket = manager.defaultSocket
        
        socket.on(clientEvent: .connect) {data, ack in
           self.socket.emit("message", "User has connected from iOS!")
           print("socket connected")
       }
        
        socket.on("voice_output_whole") { [weak self] data, ack in
            guard let self = self, let dict = data[0] as? [String: Any], let encodedString = dict["data"] as? String else { return }
            self.handleReceivedWavData(encodedString: encodedString)
        }
        socket.connect()
    }
    
    func stopConnection(){
        stopAndUploadRecording()
        socket.disconnect()
        print("Socket disconnected")
    }
    
    // Record Audio
    func startRecording() {
            let inputNode = audioEngine.inputNode
            let recordingFormat = inputNode.outputFormat(forBus: 0)
            
            do {
                // Bereite die Audiodatei vor, in die aufgenommen wird
                
                let outputAudioFilePath = documentsPath.appendingPathComponent(outputAudioFileName)
                
                
                outputFile = try AVAudioFile(forWriting: outputAudioFilePath, settings: recordingFormat.settings)
            } catch {
                print("Fehler beim Erstellen der Audiodatei: \(error)")
                return
            }
            
            // Installiere einen Tap auf dem Input Node, um das Mikrofonsignal zu erfassen
            inputNode.installTap(onBus: 0, bufferSize: 48000, format: recordingFormat) { [weak self] (buffer, when) in
                guard let self = self else { return }
                do {
                    try self.outputFile?.write(from: buffer)
                } catch {
                    print("Fehler beim Schreiben in die Audiodatei: \(error)")
                }
            }
            
            // Starte die AudioEngine
            do {
                try audioEngine.start()
                print("Aufnahme gestartet")
            } catch {
                print("AudioEngine konnte nicht gestartet werden: \(error)")
            }
        }
    
    
    func stopAndUploadRecording() {
          audioEngine.inputNode.removeTap(onBus: 0)
          audioEngine.stop()
          outputFile = nil // Schließe die Datei
          // Nach dem Stoppen der Aufnahme, lade die Datei hoch
          uploadAudioFile()
      }
      
      private func uploadAudioFile() {
          let outputAudioFilePath = documentsPath.appendingPathComponent(outputAudioFileName)
          
          guard let data = try? Data(contentsOf: outputAudioFilePath) else {
              print("Konnte Audiodatei nicht lesen")
              return
          }
          
          socket.emit("voice_input_whole", data)
          print("Audiodatei wurde gesendet")
          isRequesting = true
      }
    
    // Recive Audio
    func handleReceivedWavData(encodedString: String) {
          guard let wavData = Data(base64Encoded: encodedString) else {
              print("Fehler beim Dekodieren der WAV-Daten")
              return
          }

          do {
              print("gotResponse")
              isRequesting = false
              let recievedAudioFilePath = documentsPath.appendingPathComponent(recievedAudioFileName)
              try wavData.write(to: recievedAudioFilePath)
              print("WAV-Datei gespeichert in: \(recievedAudioFilePath.path)")
              
              // Spielen Sie die Datei sofort ab
              self.playAudio(filePath: recievedAudioFilePath)
          } catch {
              print("Fehler beim Speichern der WAV-Datei: \(error)")
          }
      }

      func playAudio(filePath: URL) {
          do {
              audioPlayer = try AVAudioPlayer(contentsOf: filePath)
              audioPlayer?.volume = 1.0
              audioPlayer?.delegate = self
              audioPlayer?.prepareToPlay()
              audioPlayer?.play()
              isPlaying = true
              print("Wiedergabe gestartet.\(isPlaying)")
              
          } catch {
              print("Fehler beim Abspielen der Audiodatei: \(error)")
          }
      }
    
    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        isPlaying = false
        print("Wiedergabe beended.\(isPlaying)")
    }
    
    func getIsPlaying() -> Bool {
        return isPlaying
    }
}
