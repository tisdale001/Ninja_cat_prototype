#pragma once

class GameObject;

class PhysicsComponent {
    public:
        // Store/get collider here?

        PhysicsComponent();

        ~PhysicsComponent();

        void UpdateX(GameObject* o);

        void UpdateY(GameObject* o);
};
