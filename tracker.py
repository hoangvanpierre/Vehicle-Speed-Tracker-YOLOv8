import math


class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        current_frame_points = {}
        
        for rect in objects_rect:
            x, y, w, h, vtype = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt_info in self.center_points.items():
                pt = pt_info[0]
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 60:
                    current_frame_points[id] = ((cx, cy), vtype)
                    objects_bbs_ids.append([x, y, w, h, id, vtype])
                    same_object_detected = True
                    # Remove from search pool so it's not reused this frame
                    del self.center_points[id]
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                current_frame_points[self.id_count] = ((cx, cy), vtype)
                objects_bbs_ids.append([x, y, w, h, self.id_count, vtype])
                self.id_count += 1

        # Update the main center_points with only objects found in current frame
        self.center_points = current_frame_points.copy()
        return objects_bbs_ids