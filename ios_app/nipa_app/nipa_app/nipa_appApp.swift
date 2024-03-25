//
//  nipa_appApp.swift
//  nipa_app
//
//  Created by Pascal Weißleder on 24.03.24.
//

import SwiftUI
import SwiftData

@main
struct nipa_appApp: App {
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            Item.self,
        ])
        let modelConfiguration = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)

        do {
            return try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()

    var body: some Scene {
        WindowGroup {
            CallView(callViewModel: CallViewModel())        }
        .modelContainer(sharedModelContainer)
    }
}
