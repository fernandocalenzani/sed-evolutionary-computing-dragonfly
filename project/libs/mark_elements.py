def mark_elements(dss, switch, transformer, regulators, capacitors):
    if (transformer == 'sim') or (transformer == 'SIM') or (transformer == 'S') or (transformer == 'y') or (transformer == 'Y') or (
            transformer == 'yes') or (transformer == 'YES'):
        dss.text("set markTransformers=Yes TransMarkerCode=17 TransMarkerSize=3")

    if (regulators == 'sim') or (regulators == 'SIM') or (regulators == 'S') or (regulators == 'y') or (
            regulators == 'Y') or (regulators == 'yes') or (regulators == 'YES'):
        dss.text("set MarkRegulators = Yes RegMarkerCode = 24 RegMarkerSize = 3")

    if (capacitors == 'sim') or (capacitors == 'SIM') or (capacitors == 'S') or (capacitors == 'y') or (
            capacitors == 'Y') or (capacitors == 'yes') or (capacitors == 'YES'):
        dss.text("set MarkCapacitors = Yes CapMarkerCode = 38 CapMarkerSize = 3")

    if (switch == 'sim') or (switch == 'SIM') or (switch == 'S') or (switch == 'y') or (switch == 'Y') or (
            switch == 'yes') or (switch == 'YES'):
        dss.text("AddBusMarker bus=150r color=blue size=3 code=37")
        dss.text("AddBusMarker bus=149  color=blue size=3 code=6")

        dss.text("AddBusMarker bus=13   color=blue size=3 code=37")
        dss.text("AddBusMarker bus=152 color=blue size=3 code=6")

        dss.text("AddBusMarker bus=18 color=blue size=3 code=37")
        dss.text("AddBusMarker bus=135 color=blue size=3 code=6")

        dss.text("AddBusMarker bus=60 color=blue size=3 code=37")
        dss.text("AddBusMarker bus=160 color=blue size=3 code=6")

        dss.text("AddBusMarker bus=97 color=blue size=3 code=37")
        dss.text("AddBusMarker bus=197 color=blue size=3 code=6")

        dss.text("AddBusMarker bus=61 color=blue size=3 code=37")
        dss.text("AddBusMarker bus=61s color=blue size=3 code=6")

        dss.text("AddBusMarker bus=151 color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=300 color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=54  color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=94  color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=95   color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=195   color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=250 color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=251 color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=450 color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=451 color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=300 color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus = 350 color = LtGray size = 3 code = 6")

    return dss
