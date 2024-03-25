//
//  Item.swift
//  nipa_app
//
//  Created by Pascal Weißleder on 24.03.24.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
