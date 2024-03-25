//
//  CallView.swift
//  nipa_app
//
//  Created by Pascal Weißleder on 24.03.24.
//

import SwiftUI

struct CallView: View {
    @ObservedObject var callViewModel: CallViewModel
    
    var body: some View {
        VStack {
            // Header
            if callViewModel.isConnected{
                Text("Connected")
                    .padding(10)
                    .background(Color.green)
                    .foregroundColor(.white)
                    .clipShape(Capsule())
            } else {
                Text("Not Connected")
                    .padding(10)
                    .foregroundColor(.white)
                    .background(Color.red)
                    .clipShape(Capsule())
            }
            if callViewModel.isRecording{
                Text("Recording...")
                    .padding(10)
                    .background(Color.green)
                    .foregroundColor(.white)
                    .clipShape(Capsule())
            } else if callViewModel.isRequesting {
                Text("Requesting...")
                    .padding(10)
                    .background(Color.orange)
                    .foregroundColor(.white)
                    .clipShape(Capsule())
            }
            if callViewModel.socketManager?.isPlaying ?? false {
                Text("Playing...")
                    .padding(10)
                    .foregroundColor(.white)
                    .background(Color.green) 
                    .clipShape(Capsule())
                    .onAppear(perform: {
                        callViewModel.resetRequesting()
                    })
            }
            
            Spacer().frame(height: 400)
            
            // Call interactions
            if callViewModel.isConnected {
                // Recording
                if callViewModel.isRecording {
                    Text("Press to stop")
                        .font(.title)
                    Button(action: {
                        callViewModel.stopRecording()
                    }, label: {
                        Image(systemName: "mic.circle.fill")
                            .resizable()
                            .foregroundColor(.red)
                            .padding(30)
                            .aspectRatio(contentMode: .fill)
                            .frame(width: 180, height: 180)
                    })
                    // Start recording
                } else if callViewModel.socketManager?.isPlaying ?? false {
                    Text("Your response")
                        .font(.title)
                    Image(systemName: "message.badge.waveform")
                        .resizable()
                        .foregroundColor(.white)
                        .padding(30)
                        .background(Color.green)
                        .cornerRadius(38)
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 150, height: 150)
                }
                else if callViewModel.isRequesting {
                    Text("Wait on response")
                        .font(.title)
                    Image(systemName: "arrow.triangle.2.circlepath.icloud.fill")
                        .resizable()
                        .foregroundColor(.white)
                        .padding(30)
                        .background(Color.orange)
                        .cornerRadius(38)
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 150, height: 150)
                    Button(action: {
                        callViewModel.endCall()
                    }, label: {
                        Text("Cancel")
                            .padding(10)
                            .foregroundColor(.white)
                            .background(Color.red)
                            .clipShape(Capsule())
                    })
                }
                // Playing
                
                
                else {
                    Text("Press to ask more")
                        .font(.title)
                    Button(action: {
                        callViewModel.startRecording()
                    }, label: {
                        Image(systemName: "mic.circle.fill")
                            .resizable()
                            .foregroundColor(.blue)
                            .padding(30)
                            .aspectRatio(contentMode: .fill)
                            .frame(width: 180, height: 180)
                    }) 
                    Button(action: {
                        callViewModel.endCall()
                    }, label: {
                        Text("Disconnect")
                            .padding(10)
                            .foregroundColor(.white)
                            .background(Color.red)
                            .clipShape(Capsule())
                    })
                }
                
            } else {
                Text("Press to ask")
                    .font(.title)
                Button(action: {
                    callViewModel.startCall()
                    callViewModel.startRecording()
                }, label: {
                    Image(systemName: "mic.circle.fill")
                        .resizable()
                        .padding(30)
                        .foregroundColor(.blue)
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 180, height: 180)
                })
            }
        }.background( 
            VStack{
                Spacer()
                    .frame(height: 130)
                Image("canton_logo")
                    .resizable()
                    .edgesIgnoringSafeArea(.all)
                    .scaledToFit()
                    .frame(width: 200, height: 400)
                Spacer()
                    .frame(height: 350)
                
            }
        )
    }
}

struct CallView_Previews: PreviewProvider {
    static var previews: some View {
        CallView(callViewModel: CallViewModel())
    }
}
