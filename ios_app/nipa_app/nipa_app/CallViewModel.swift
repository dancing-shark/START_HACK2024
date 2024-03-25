//
//  CallViewModel.swift
//  nipa_app
//
//  Created by Pascal Weißleder on 24.03.24.
//

import Foundation
import Combine
// Import necessary modules for WebSocket and AVFoundation

class CallViewModel: ObservableObject {
    
    @Published var isConnected = false
    
    @Published var isRecording = false
    @Published var isRequesting = false
    @Published var isPlayingRep = false
    
    
    
    var socketManager: SocketIOManager?
    
    private var cancellables = Set<AnyCancellable>()
    
    private func setupObservers() {
            // Ensure socketManager exists and then subscribe to the `isPlaying` property
            socketManager?.$isPlaying
                .receive(on: DispatchQueue.main) // Ensure UI updates on main thread
                .assign(to: \.isPlayingRep, on: self)
                .store(in: &cancellables)
        }
    

    func startCall() {
        isConnected = true
        self.socketManager = SocketIOManager()
        setupObservers()
    }
    
    func endCall() {
        isConnected = false
        isRecording = false
        isRequesting = false
        // Stop the audio streamer
        socketManager?.stopConnection()
        socketManager = nil
        
    }
    
    func startRecording(){
        guard socketManager != nil else {
            return
        }
        isRecording = true
        socketManager?.startRecording()
    }
    
    func stopRecording(){
        guard socketManager != nil else {
            return
        }
        isRecording = false
        socketManager?.stopAndUploadRecording()
        isRequesting = true
        
    }
    func isPlaying() -> Bool {
        guard let manager = socketManager else {
            return false
        }
        print(manager.getIsPlaying())
        return manager.getIsPlaying()
    }
    func resetRequesting() {
        isRequesting = false
    }
    
    
}

